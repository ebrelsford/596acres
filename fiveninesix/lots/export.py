import csv
import simplekml
import StringIO

def to_csv(lots):
    """
    Get CSV string for the given lots.
    """

    # TODO use fields and their verbose names for the header
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

    csv_string = StringIO.StringIO()
    csv_file = csv.DictWriter(csv_string, fields)

    csv_string.write(','.join(["%s" % field for field in fields]))
    csv_string.write('\n')
    for lot in lots:
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

    return csv_string.getvalue()

def to_kml(lots):
    """
    Get KML for the given lots.
    """
    kml = simplekml.Kml()

    for lot in lots:
        kml.newpoint(
            name=lot.bbl, 
            description="bbl: %s<br/>agency: %s<br/>area: %f acres" % (
                lot.bbl,
                lot.owner.name,
                lot.area_acres or 0
            ), 
            coords=[(lot.centroid.x, lot.centroid.y)]
        )

    return kml.kml(format=False)
