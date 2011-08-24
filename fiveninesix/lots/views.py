from datetime import date
import geojson
import json
from random import randint
import simplekml

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from models import Lot, Owner

def lot_geojson(request):
    lots = _filter_lots(request).values('bbl', 'area', 'centroid', 'organizer', 'actual_use')
    lots_geojson = _lot_collection(lots)

    response = HttpResponse(mimetype='application/json')
    if 'download' in request.GET and request.GET['download'] == 'true':
        response['Content-Disposition'] = 'attachment; filename="596acres (%s).geojson"' % date.today().strftime('%m-%d-%Y')
    response.write(geojson.dumps(lots_geojson))
    return response

def lot_kml(request):
    """Download lots as KML, filtered using the given request"""
    kml = simplekml.Kml()
    
    for lot in _filter_lots(request):
        kml.newpoint(
            name=lot.bbl, 
            description="bbl: %s<br/>agency: %s<br/>area: %f square feet" % (lot.bbl, lot.owner.name, lot.area), 
            coords=[(lot.centroid.x, lot.centroid.y)]
        )

    response = HttpResponse(mimetype='application/vnd.google-earth.kml+xml')
    if 'download' in request.GET and request.GET['download'] == 'true':
        response['Content-Disposition'] = 'attachment; filename="596acres (%s).kml"' % date.today().strftime('%m-%d-%Y')
    response.write(kml.kml(format=False))
    return response

def _filter_lots(request):
    mapped_lots = Lot.objects.filter(centroid__isnull=False)
    lots = mapped_lots

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
    if 'lot_type' in request.GET:
        lot_types = request.GET['lot_type'].split(',')
        lots_vacant = lots.filter(is_vacant=True)
        lots_garden = lots.filter(actual_use__startswith='Garden')
        if 'vacant' in lot_types and 'garden' in lot_types:
            lots = lots_vacant | lots_garden
        else:
            if 'vacant' in lot_types:
                lots = lots_vacant
            if 'garden' in lot_types:
                lots = lots_garden

    return lots

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
        lot['bbl'],
        geometry=geojson.Point(coordinates=(lot['centroid'].x, lot['centroid'].y)),
        properties={
            'area': float(lot['area']),
            'is_garden': lot['actual_use'] and lot['actual_use'].startswith('Garden'),
            'has_organizers': lot['organizer'] is not None,
        },
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
