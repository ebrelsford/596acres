import json
import pyproj
import urllib2

from django.conf import settings
from django.contrib.gis.geos import Point

from lots.models import Lot, Owner

LCC = pyproj.Proj('+proj=lcc +lat_1=41.03333333333333 +lat_2=40.66666666666666 '
                  '+lat_0=40.16666666666666 +lon_0=-74 +x_0=300000 +y_0=0 '
                  '+ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 '
                  '+no_defs')

METERS_PER_FOOT = 0.304800609012192

def convert_coordinates_to_lon_lat(x, y):
    if x != 0 and y != 0:
        (lon, lat) = LCC(x, y, inverse=True)
        return (lon, lat)

def convert_lon_lat_to_coordinates(lon, lat):
    (x, y) = LCC(lon, lat)
    return [c / METERS_PER_FOOT for c in (x, y)]

def convert_sq_ft_to_acres(sq_ft):
    return sq_ft / 43560.0

def make_bbl(borough, block, lot):
    return "%d%05d%04d" % (borough, block, lot)

def halfway(max_a, min_a):
    return ((max_a - min_a) / 2) + min_a

def approximate_coordinates(obj):
    return (halfway(obj['MaxX'], obj['MinX']), halfway(obj['MaxY'], obj['MinY']))

def get_oasis_data(bbl):
    response = urllib2.urlopen(settings.OASIS_DATA_URL % bbl)
    return json.loads(response.read())[0][0]

def get_coordinates(bbl):
    return get_coordinates_from_response(get_oasis_data(bbl))

def get_lon_lat_for_bbl(bbl):
    oasis_data = get_oasis_data(bbl)
    (x, y) = get_coordinates_from_response(oasis_data)
    (lon, lat) = convert_coordinates_to_lon_lat(x, y)
    return (lon, lat)

def get_coordinates_from_response(oasis_response):
    (x, y) = (oasis_response['XCoord'], oasis_response['YCoord'])
    if x == 0 or y == 0:
        (x, y) = approximate_coordinates(oasis_response['Extent'])
    return [c * METERS_PER_FOOT for c in (x, y)]

def add_centroid(lot):
    (lon, lat) = get_lon_lat_for_bbl(lot.bbl)
    lot.centroid = Point(float(lon), float(lat))
    lot.save()

def load_from_oasis(bbl, owner_name=None):
    # ensure bbl does not exist
    if Lot.objects.filter(bbl=bbl).count() > 0:
        print 'Lot with bbl %s already exists!' % bbl
        return

    oasis_data = get_oasis_data(bbl)
    (x, y) = get_coordinates_from_response(oasis_data)
    (lon, lat) = convert_coordinates_to_lon_lat(x, y)

    if not owner_name:
        owner_name = oasis_data['OwnerName']
    try:
        owner = Owner.objects.get(name=owner_name)
    except Exception:
        owner = Owner.objects.get(oasis_name=owner_name)

    lot = Lot(
        address=oasis_data['Address'],
        area=oasis_data['Area'],
        area_acres=str(convert_sq_ft_to_acres(oasis_data['Area'])),
        bbl=bbl,
        block=oasis_data['Block'],
        borough=oasis_data['BoroughName'],
        centroid=Point(float(lon), float(lat)),
        city_council_district=oasis_data['CityCouncilDistrict'],
        lot=oasis_data['Lot'],
        owner=owner,
        police_precinct=oasis_data['PolicePrecinct'],
        zipcode=oasis_data['ZipCode']
    )
    lot.save()
    print 'Successfully added lot %s.' % bbl
