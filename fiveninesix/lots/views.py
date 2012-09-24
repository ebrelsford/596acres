import csv
from datetime import date
import geojson
import json
from random import randint
import simplekml

from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import Distance
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.cache import cache_page

from django_xhtml2pdf.utils import render_to_pdf_response

from forms import ReviewForm
from models import Lot, Owner, Review, LOT_QS
from organize.models import Note, Organizer, Watcher
from photos.models import PhotoAlbum
from settings import BASE_URL, OASIS_BASE_URL

def lot_geojson(request):
    cacheable = _is_base_geojson_request(request.GET)
    cache_key = 'lots__views:lots_geojson:base'
    geojson_response = None
    if cacheable:
        geojson_response = cache.get(cache_key)

    if not geojson_response:
        filters = _request_to_filters(request)
        lots = _filter_lots(filters).distinct().select_related('owner', 'owner__type').annotate(Count('organizer'))
        recent_changes = _recent_changes()
        lots_geojson = _lot_collection(lots, recent_changes)
        geojson_response = geojson.dumps(lots_geojson)
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
        params['lot_types'] = params['lot_types'].split(',')
    except:
        params['lot_types'] = ['vacant','organizing','accessed','private_accessed']

    try:
        params['owner_types'] = params['owner_type'].split(',')
    except:
        params['owner_types'] = ['city', 'private']
    if 'private_accessed' not in params['lot_types'] and 'private' in params['owner_types']:
        params['owner_types'].remove('private')

    try:
        boroughs = [b.title() for b in params['boroughs'].split(',')]
        if not request.user.is_authenticated():
            if any(map(lambda b: b not in settings.PUBLIC_BOROUGHS, boroughs)):
                raise Exception('Only logged-in users can view all boroughs.')
        params['boroughs'] = boroughs
    except:
        params['boroughs'] = settings.PUBLIC_BOROUGHS

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

    lot_types = filters['lot_types']
    if len(lot_types) > 0:
        lots_by_lot_type = Lot.objects.none()
        for lot_type in lot_types:
            if lot_type in LOT_QS:
                lots_by_lot_type = lots_by_lot_type | Lot.objects.filter(LOT_QS[lot_type])
        lots = lots & lots_by_lot_type

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
        'lot': lot,
        'review': review,
        'organizers': lot.organizer_set.all(),
        'watchers_count': lot.watcher_set.all().count(),
        'notes': lot.note_set.all().order_by('added'),
        'photo_albums': PhotoAlbum.objects.filter(
            content_type=ContentType.objects.get_for_model(lot),
            object_id=lot.pk,
        ).all(),
        'pictures': lot.picture_set.all().order_by('added'),
        'OASIS_BASE_URL': OASIS_BASE_URL,
    }, context_instance=RequestContext(request))

def owner_details(request, id=None):
    owner = get_object_or_404(Owner, id=id)
    details = owner.__dict__
    for k in details.keys():
        if k.startswith('_'):
            del details[k]
    return HttpResponse(json.dumps(details), mimetype='application/json')

def _lot_collection(lots, recent_changes):
    return geojson.FeatureCollection(features=[_lot_feature(lot, recent_changes) for lot in lots])

def _lot_feature(lot, recent_changes):
    change = None
    if lot.id in recent_changes:
        change = recent_changes[lot.id].recent_change_label()

    try:
        # XXX lot.lots_area_acres makes extra DB queries
        area = round(float(lot.lots_area_acres), 3)
    except Exception:
        area = 0

    properties={
        'area': area,
        'is_garden': lot.actual_use and lot.actual_use.startswith('Garden'),
        'has_organizers': lot.organizer__count > 0,
        'group_has_access': lot.group_has_access,
        'recent_change': change,
        'accessible': lot.accessible,
        'actual_use': lot.actual_use,
        'owner_type': lot.owner.type.name,
    }

    return geojson.Feature(
        lot.bbl,
        geometry=geojson.Point(coordinates=(lot.centroid.x, lot.centroid.y)),
        properties=properties
    )

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

def organizing(request):
    lots = Lot.objects.filter(is_vacant=True).exclude(organizer=None)

    return render_to_response('lots/list.html', {
        'lots': lots,
    }, context_instance=RequestContext(request))

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

def counts(request):
    """
    Get counts of each lot type for the given boroughs.
    """
    # unset parents_only as counts use parents and children
    filters = _request_to_filters(request, { 'parents_only': 'false' })
    lots = _filter_lots(filters)
    lot_types = (
        'accessed_lots',
        'accessed_sites',
        'garden_lots',
        'garden_sites',
        'gutterspace',
        'organizing_lots',
        'organizing_sites',
        'private_accessed_lots',
        'private_accessed_sites',
        'vacant_lots',
        'vacant_sites',
    )
    c = {}
    for lot_type in lot_types:
        c[lot_type] = (lots & Lot.objects.filter(LOT_QS[lot_type]).distinct()).count()

    acres_lot_types = (
        'accessed_lots',
        'garden_lots',
        'gutterspace',
        'organizing_lots',
        'private_accessed_lots',
        'vacant_lots',
    )
    for lot_type in acres_lot_types:
        ls = lots & Lot.objects.filter(LOT_QS[lot_type]).distinct()

        # XXX NB: A little ugly, to sum over distinct lots. All of these 
        # queries could be optimized.
        acres = Lot.objects.filter(pk__in=ls).aggregate(acres=Sum('area_acres'))['acres']
        if not acres:
            acres = 0
        c[lot_type + '_acres'] = str(round(acres, 3))

    return HttpResponse(json.dumps(c), mimetype='application/json')

def _is_base_geojson_request(GET):
    non_base_params = ('owner_code', 'owner_id', 'bbls', 'min_area',
                       'max_area', 'source')
    if any([GET.get(x, False) for x in non_base_params]):
        return False
    return (GET.get('lot_types', '') == 'vacant,organizing,accessed,private_accessed' and
            GET.get('boroughs', '') == 'Brooklyn,Manhattan,Queens' and
            GET.get('parents_only', 'false') == 'true')
