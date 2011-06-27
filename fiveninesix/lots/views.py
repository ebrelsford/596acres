import geojson
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from models import Lot, Owner, OwnerType

def lot_geojson(request):
    lots = Lot.objects.filter(centroid__isnull=False)

    if 'source' in request.GET:
        lots = lots.filter(centroid_source=request.GET['source'])
    if 'owner_code' in request.GET:
        lots = lots.filter(owner__code=request.GET['owner_code'])

    lots_geojson = _lot_collection(lots)
    return HttpResponse(geojson.dumps(lots_geojson), mimetype='application/json')

def details(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    details = {
        'address': lot.address,
        'bbl': lot.bbl,
        'block': lot.block,
        'lot': lot.lot,
        'zipcode': lot.zipcode,
        'owner': lot.owner.name,
        'area': float(lot.area),
    }
    return HttpResponse(json.dumps(details), mimetype='application/json')

def _lot_collection(lots):
    return geojson.FeatureCollection(features=[_lot_feature(lot) for lot in lots])

def _lot_feature(lot):
    return geojson.Feature(
        lot.bbl,
        geometry=geojson.Point(coordinates=(lot.centroid.x, lot.centroid.y))
    )

