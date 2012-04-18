import pyproj

lcc = pyproj.Proj('+proj=lcc +lat_1=41.03333333333333 +lat_2=40.66666666666666 +lat_0=40.16666666666666 +lon_0=-74 +x_0=300000.0000000001 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs')

def convert_coordinates_to_lon_lat(x, y):
    if x != 0 and y != 0:
        (lon, lat) = lcc(x, y, inverse=True)
        return (lon, lat)

def convert_sq_ft_to_acres(sq_ft):
    return sq_ft / 43560.0

def make_bbl(borough, block, lot):
    return "%d%05d%04d" % (borough, block, lot)
