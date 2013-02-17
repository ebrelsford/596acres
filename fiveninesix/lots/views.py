import csv
from datetime import date
import json
from random import randint
import simplekml

from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import Distance
from django.db.models import Count, Sum, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.cache import cache_page

from django_xhtml2pdf.utils import render_to_pdf_response

from forms import ReviewForm
from lots.load import convert_lon_lat_to_coordinates
from lots.util import get_nearby
from models import Lot, LotLayer, Owner, Review
from organize.models import Note, Organizer, Watcher
from photos.models import PhotoAlbum
from settings import BASE_URL, OASIS_BASE_URL

def lot_geojson(request):
    cacheable = _is_base_geojson_request(request.GET)

    cache_key = 'lots__views:lots_geojson:base'
    geojson_response = None
    if cacheable:
        geojson_response = cache.get(cache_key)

    # TODO consider downloading everything at once, doing filtering client-side
    if not geojson_response:
        filters = _request_to_filters(request)
        print filters

        lots = _filter_lots(filters).distinct()
        lots = lots.select_related('owner', 'owner__type')
        lots = lots.annotate(Count('organizer'))

        layers = LotLayer.objects.all().values_list('name', flat=True)

        for layer in layers:
            lots = lots.extra(
                select={
                    layer: 'lots_lotlayer.name=%s',
                },
                select_params=[
                    layer,
                ]
            )

        recent_changes = _recent_changes()
        lots_geojson = _lot_collection(lots, recent_changes, layers=layers)
        geojson_response = json.dumps(lots_geojson)

        if cacheable:
            cache.set(cache_key, geojson_response, 6 * 60 * 60)

    response = HttpResponse(mimetype='application/json')
    if 'download' in request.GET and request.GET['download'] == 'true':
        response['Content-Disposition'] = 'attachment; filename="596acres (%s).geojson"' % date.today().strftime('%m-%d-%Y')
    response.write(geojson_response)
    return response

def lot_kml(request):
    """Download lots as KML, filtered using the given request"""
    # TODO use export.to_kml()
    kml = simplekml.Kml()

    filters = _request_to_filters(request)
    for lot in _filter_lots(filters):
        kml.newpoint(
            name=lot.bbl,
            description="bbl: %s<br/>agency: %s<br/>area: %f acres" % (
                lot.bbl,
                lot.owner.name,
                lot.area_acres or 0
            ),
            coords=[(lot.centroid.x, lot.centroid.y)]
        )

    response = HttpResponse(mimetype='application/vnd.google-earth.kml+xml')
    if 'download' in request.GET and request.GET['download'] == 'true':
        response['Content-Disposition'] = 'attachment; filename="596acres (%s).kml"' % date.today().strftime('%m-%d-%Y')
    response.write(kml.kml(format=False))
    return response

def lot_csv(request):
    response = HttpResponse(mimetype='text/csv')

    fields = (
        'address',
        'borough',
        'bbl',
        'block',
        'lot',
        'zipcode',
        'agency/owner name',
        'area (sq ft)',
        'area (acres)',
        'is vacant',
        'actual use',
        'group has access',
        'accessible',
        'longitude',
        'latitude',
    )

    csv_file = csv.DictWriter(response, fields)

    response.write(','.join(["%s" % field for field in fields]))
    response.write('\n')

    filters = _request_to_filters(request)
    for lot in _filter_lots(filters):
        try:
            csv_file.writerow({
                'address': lot.address,
                'borough': lot.borough,
                'bbl': lot.bbl,
                'block': lot.block,
                'lot': lot.lot,
                'zipcode': lot.zipcode,
                'agency/owner name': lot.owner.name,
                'area (sq ft)': lot.area,
                'area (acres)': lot.area_acres,
                'is vacant': lot.is_vacant,
                'actual use': lot.actual_use,
                'group has access': lot.group_has_access,
                'accessible': lot.accessible,
                'longitude': lot.centroid.x,
                'latitude': lot.centroid.y,
            })
        except:
            continue

    response['Content-Disposition'] = 'attachment; filename="596 Acres %s lots%s.csv"' % (date.today().strftime('%m-%d-%Y'), _get_filter_description(request))
    return response

def _get_filter_description(request):
    """Get a description of the filters being viewed in the given request."""
    description = ''
    if 'lot_type' in request.GET:
        description += ' ' + request.GET['lot_type']
    if 'owner_id' in request.GET:
        owner = Owner.objects.get(pk=request.GET['owner_id'])
        description += ' owned by ' + owner.name
    return description

def _request_to_filters(request, override={}):
    """
    Pre-process a request to be lot filters.
    """
    params = request.GET.copy()
    params.update(override)

    try:
        if not params['lot_types']:
            params['lot_types'] = []
        params['lot_types'] = params['lot_types'].split(',')
    except Exception:
        params['lot_types'] = []

    try:
        params['owner_types'] = params['owner_type'].split(',')
    except Exception:
        params['owner_types'] = ['city', 'private']

    try:
        boroughs = [b.title() for b in params['boroughs'].split(',')]
        if not request.user.is_authenticated():
            if any(map(lambda b: b not in settings.PUBLIC_BOROUGHS, boroughs)):
                raise Exception('Only logged-in users can view all boroughs.')
        params['boroughs'] = boroughs
    except Exception:
        params['boroughs'] = settings.PUBLIC_BOROUGHS

    try:
        params['owners'] = params['owners'].split(',')
    except Exception:
        pass

    try:
        params['user_types'] = params['user_types'].split(',')
    except Exception:
        pass

    if 'source' in params:
        if params['source'] != 'all':
            params['source'] = params['source'].split(',')

    if 'bbls' in params:
        params['bbls'] = params['bbls'].split(',')

    params['parents_only'] = params.get('parents_only', 'false') == 'true'

    if 'max_area' in params:
        max_area = params['max_area']
        if max_area < 3:
            params['max_area'] = 3

    if 'bbox' in params:
        params['bbox'] = Polygon.from_bbox(params['bbox'].split(','))

    return params

def _filter_lots(filters):
    """
    Filter lots with the given dict of filters.
    """
    mapped_lots = Lot.objects.filter(centroid__isnull=False)
    lots = mapped_lots

    if 'boroughs' in filters:
        lots = lots.filter(borough__in=filters['boroughs'])
    if 'source' in filters:
        lots = lots.filter(centroid_source__in=filters['source'])
    if 'owner_code' in filters:
        lots = lots.filter(owner__code=filters['owner_code'])
    if 'owner_id' in filters:
        lots = lots.filter(owner__id=filters['owner_id'])
    if 'bbls' in filters:
        bbls = filters['bbls']
        if len(bbls) == 1 and filters.get('with_nearby_lots', 'no') == 'yes':
            target_lots = Lot.objects.filter(centroid__isnull=False, bbl=bbls[0])
            if target_lots:
                lots = lots.filter(centroid__distance_lte=(target_lots[0].centroid, Distance(mi=.25)))
            else:
                lots = Lot.objects.none()
        else:
            lots = lots.filter(bbl__in=bbls)
    if 'parents_only' in filters and filters['parents_only']:
        lots = lots.filter(parent_lot__isnull=True)
    if 'min_area' in filters:
        lots = lots.filter(area_acres__gte=filters['min_area'])
    if 'max_area' in filters:
        lots = lots.filter(area_acres__lte=filters['max_area'])
    if 'bbox' in filters:
        lots = lots.filter(centroid__within=filters['bbox'])
    if 'owner_types' in filters and filters['owner_types']:
        lots = lots.filter(owner__type__name__in=filters['owner_types'])
    if 'owners' in filters and filters['owners']:
        lots = lots.filter(owner__name__in=filters['owners'])
    if 'user_types' in filters and filters['user_types']:
        user_types = filters['user_types']
        user_filters = Q()
        if 'organizers' in user_types:
            user_filters = user_filters | Q(organizer__isnull=False)
        if 'watchers' in user_types:
            user_filters = user_filters | Q(watcher__isnull=False)
        lots = lots.filter(user_filters)
    if 'lot_types' in filters and filters['lot_types']:
        lots = lots.filter(lotlayer__name__in=filters['lot_types'])

    return lots.distinct()

def details_json(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    details = {
        'address': lot.address,
        'bbl': lot.bbl,
        'block': lot.block,
        'lot': lot.lot,
        'zipcode': lot.zipcode,
        'owner': lot.owner.name,
        'owner_id': lot.owner.id,
        'area': float(lot.area_acres),
    }
    return HttpResponse(json.dumps(details), mimetype='application/json')

@cache_page(12 * 60 * 60)
def owners_json(request):
    owners = {
        'owners': list(Owner.objects.filter(type__name='city').values_list('id', 'name').order_by('name')),
    }
    return HttpResponse(json.dumps(owners), mimetype='application/json')

def details(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)

    # if lot has a parent (and on...), redirect to that
    l = lot.get_oldest_ancestor()
    if l != lot:
        return redirect('lots.views.details', bbl=l.bbl)

    review = Review.objects.filter(lot=lot).order_by('-added')
    if review:
        review = review[0]

    return render_to_response('lots/details.html', {
        'BASE_URL': settings.BASE_URL,
        'lot': lot,
        'nearby_lots': get_nearby(lot),
        'notes': lot.note_set.all().order_by('added'),
        'OASIS_BASE_URL': OASIS_BASE_URL,
        'organizers': lot.organizer_set.all(),
        'photo_albums': PhotoAlbum.objects.filter(
            content_type=ContentType.objects.get_for_model(lot),
            object_id=lot.pk,
        ).all(),
        'pictures': lot.picture_set.all().order_by('added'),
        'review': review,
        'watchers_count': lot.watcher_set.all().count(),
    }, context_instance=RequestContext(request))

def owner_details(request, id=None):
    owner = get_object_or_404(Owner, id=id)
    details = owner.__dict__
    for k in details.keys():
        if k.startswith('_'):
            del details[k]
    return HttpResponse(json.dumps(details), mimetype='application/json')

def _lot_collection(lots, recent_changes, layers=[]):
    features = [_lot_feature(lot, recent_changes, layers=layers) for lot in lots]
    return {
        'features': features,
        'type': 'FeatureCollection',
    }

def _lot_feature(lot, recent_changes, layers=[]):
    try:
        # XXX lot.lots_area_acres makes extra DB queries
        # TODO cache on a 'through' table
        #area = round(float(lot.lots_area_acres), 3)
        area = round(float(lot.area_acres), 3)
    except Exception:
        area = 0

    # Bare minimum properties. Avoid adding others unless they're significant
    # to reduce output size.
    properties = {
        'area': area,
    }

    if lot.id in recent_changes:
        properties.update({
            'recent_change': recent_changes[lot.id].recent_change_label(),
        })

    for layer in layers:
        try:
            if getattr(lot, layer):
                properties.update({
                    layer: True,
                })
        except Exception:
            pass

    return {
        'id': lot.bbl,
        'geometry': {
            'type': 'Point',
            'coordinates': [lot.centroid.x, lot.centroid.y],
        },
        'properties': properties,
        'type': 'Feature',
    }

def _recent_changes(maximum=5):
    """Find recent changes globally, keyed by lot id"""

    objs = []
    for T in (Organizer, Note, Watcher):
        objs += list(T.objects.all().order_by('-added')[:maximum])
    objs.sort(cmp=lambda x, y: -cmp(x.added, y.added))
    objs = objs[:maximum]

    changes = {}
    for obj in objs:
        try:
            changes[obj.lot.id] = obj
        except:
            try:
                changes[obj.lots.all()[0].id] = obj
            except:
                continue

    return changes

def tabs(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    photo = None
    try:
        photo = PhotoAlbum.objects.filter(
            content_type=ContentType.objects.get_for_model(lot),
            object_id=lot.pk,
        ).all()[0].get_cover_photo()
    except Exception:
        pass

    return render_to_response('lots/tabs.html', {
        'lot': lot,
        'organizers': lot.organizer_set.all(),
        'photo': photo,
        'pictures': lot.picture_set.all().order_by('added'),
        'watchers_count': lot.watcher_set.all().count(),
        'OASIS_BASE_URL': OASIS_BASE_URL,
    }, context_instance=RequestContext(request))

def oasis_popup(request):
    try:
        address = request.GET['address']
    except KeyError:
        address = None
    try:
        latitude = request.GET['latitude']
    except KeyError:
        latitude = None
    try:
        longitude = request.GET['longitude']
    except KeyError:
        longitude = None
    try:
        query = request.GET['query']
    except KeyError:
        query = None

    x, y = convert_lon_lat_to_coordinates(float(longitude), float(latitude))
    oasis_url = settings.OASIS_LAT_LON_URL + 'x=%f&y=%f' % (x, y)

    return render_to_response('lots/oasis_popup.html', {
        'address': address,
        'oasis_url': oasis_url,
        'query': query,
    }, context_instance=RequestContext(request))

def random(request):
    bbls = Lot.objects.filter(
        accessible=True,
        actual_use=None,
        centroid__isnull=False,
        is_vacant=True,
        owner__type__name='city',
        borough__in=settings.PUBLIC_BOROUGHS,
    ).values_list('bbl', flat=True)
    return redirect('lots.views.details', bbl=bbls[randint(0, bbls.count() - 1)])

def pdf(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    lot.generate_qrcode()

    return render_to_pdf_response('lots/pdf.html', context=RequestContext(request, {
        'lot': lot,
        'base_url': BASE_URL,
        'organizers': lot.organizer_set.all(),
    }), pdfname='596acres:%s.pdf' % lot.bbl)

def qrcode(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    lot.generate_qrcode()

    response = HttpResponse(mimetype='image/png')
    response.write(lot.qrcode.read())
    return response

@permission_required('lots.add_review')
def add_review(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lots.views.details', bbl=bbl)
    else:
        initial_data = {
            'reviewer': request.user,
            'lot': lot,
            'in_use': not lot.is_vacant,
            'actual_use': lot.actual_use,
        }

        reviews = Review.objects.filter(lot=lot).order_by('-added')
        fields = ('in_use', 'actual_use', 'accessible', 'needs_further_review',
                  'nearby_lots', 'hpd_plans', 'hpd_plans_details')
        if reviews:
            last_review = reviews[0]
            for field in fields:
                initial_data[field] = last_review.__dict__[field]

        form = ReviewForm(initial=initial_data)

    return render_to_response('lots/add_review.html', {
        'form': form,
        'lot': lot,
    }, context_instance=RequestContext(request))

def _lot_type_prefix(lot_type):
    return '_'.join(lot_type.split('_')[:-1])

def counts(request):
    """
    Get counts of each lot type for the given boroughs.
    """
    # hold on to requested lot types
    lot_types = request.GET.get('lot_types', [])
    if lot_types: lot_types = lot_types.split(',')
    lot_types = [_lot_type_prefix(t) for t in lot_types]

    # unset parents_only as counts use parents and children
    filters = _request_to_filters(request, {
        'lot_types': '',
        'owner_types': 'city,private',
        'parents_only': 'false',
    })
    lots = _filter_lots(filters)
    totals = lots.values('lotlayer__name').annotate(
        area=Sum('area_acres'),
        count=Count('pk'),
    )

    # fill with 0 as default
    c = {}
    for layer in LotLayer.objects.all():
        c.update({
            layer.name: 0,
            layer.name + '_acres': 0,
        })

    for row in totals:
        layer = row['lotlayer__name']
        if not layer or not _lot_type_prefix(layer) in lot_types: continue

        count = row['count']
        try:
            area = str(round(row['area'], 3))
        except Exception:
            area = 0

        c.update({
            layer: count,
            layer + '_acres': area,
        })

    return HttpResponse(json.dumps(c), mimetype='application/json')

def _is_base_geojson_request(GET):
    non_base_params = (
        'bbls',
        'max_area',
        'min_area',
        'owner_code',
        'owner_id',
        'source',
    )

    base_lot_types = (
        'organizing_sites',
        'private_accessed_sites',
        'public_accessed_sites',
        'vacant_sites',
    )

    base_boroughs = (
        'Brooklyn',
        'Manhattan',
        'Queens',
    )

    if any([GET.get(x, False) for x in non_base_params]):
        return False
    return all((
        sorted(GET.get('lot_types', '').split(',')) == base_lot_types,
        sorted(GET.get('boroughs', '').split(',')) == base_boroughs,
        GET.get('parents_only', 'false') == 'true'
    ))
