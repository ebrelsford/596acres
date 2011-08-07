import geojson
import json
from random import randint

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from models import Lot, Owner, OwnerType

def lot_geojson(request):
    lots = Lot.objects.filter(centroid__isnull=False, is_vacant=True)

    if 'source' in request.GET:
        sources = request.GET['source'].split(',')
        lots = lots.filter(centroid_source__in=sources)
    if 'owner_type' in request.GET:
        lots = lots.filter(owner__type__name=request.GET['owner_type'])
    if 'owner_code' in request.GET:
        lots = lots.filter(owner__code=request.GET['owner_code'])
    if 'owner_id' in request.GET:
        lots = lots.filter(owner__id=request.GET['owner_id'])
    if 'bbls' in request.GET:
        bbls = request.GET['bbls'].split(',')
        lots = lots.filter(bbl__in=bbls)
    if 'min_area' in request.GET:
        lots = lots.filter(area__gte=request.GET['min_area'])
    if 'max_area' in request.GET:
        max_area = request.GET['max_area']
        if max_area < 100000:
            lots = lots.filter(area__lte=max_area)

    lots_geojson = _lot_collection(lots)
    return HttpResponse(geojson.dumps(lots_geojson), mimetype='application/json')

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
        'area': float(lot.area),
    }
    return HttpResponse(json.dumps(details), mimetype='application/json')

def owners_json(request):
    owners = {
        'owners': list(Owner.objects.filter(type__name='city').values_list('id', 'name').order_by('name')),
    }
    return HttpResponse(json.dumps(owners), mimetype='application/json')


def details(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    return render_to_response('lots/details.html', {
        'lot': lot,
        'organizers': lot.organizer_set.all()
    }, context_instance=RequestContext(request))

def owner_details(request, id=None):
    owner = get_object_or_404(Owner, id=id)
    details = owner.__dict__
    for k in details.keys():
        if k.startswith('_'):
            del details[k]
    return HttpResponse(json.dumps(details), mimetype='application/json')

def _lot_collection(lots):
    return geojson.FeatureCollection(features=[_lot_feature(lot) for lot in lots])

def _lot_feature(lot):
    return geojson.Feature(
        lot.bbl,
        geometry=geojson.Point(coordinates=(lot.centroid.x, lot.centroid.y)),
        properties={
            'area': float(lot.area),
        }
    )

def tabs(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)

    return render_to_response('lots/tabs.html', {
        'lot': lot,
        'organizers': lot.organizer_set.all()
    }, context_instance=RequestContext(request))

def random(request):
    bbls = Lot.objects.filter(is_vacant=True, centroid_source__in=('OASIS', 'Google', 'Nominatim'), owner__type__name='city').values_list('bbl', flat=True)
    return redirect(details, bbl=bbls[randint(0, bbls.count())])
