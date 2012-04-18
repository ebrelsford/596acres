# encoding: utf-8
import csv
from south.v2 import DataMigration

from lots import load
from django.contrib.gis.geos import Point

class Migration(DataMigration):

    def _get_centroid(self, lot):
        lon, lat = lot['lon'], lot['lat']
        if not lon or not lat:
            x, y = int(lot['X Coordinate']), int(lot['Y Coordinate'])
            lon, lat = load.convert_coordinates_to_lon_lat(x, y)
        else:
            lon, lat = float(lot['lon']), float(lot['lat'])
        return Point(lon, lat)

    def forwards(self, orm):
        "Write your forwards methods here."
        owner = orm.Owner.objects.get(name='Housing Preservation and Development')
        for lot in csv.DictReader(open('../data/HPD-owned Parking Facilities 2011 actually parking.csv', 'r')):
            if lot['Vacant'] != 'yes':
                continue

            bbl = load.make_bbl(3, int(lot['Block']), int(lot['Lot']))
            if orm.Lot.objects.filter(bbl=bbl).count() > 0:
                print "Lot %s already exists. Skipping." % bbl
                continue

            saved_lot = orm.Lot(
                address=lot['Address'],
                borough='Brooklyn',
                bbl=bbl,
                block=lot['Block'],
                lot=lot['Lot'],
                zipcode=lot['ZipCode'],
                owner=owner,
                area=lot['Lot Area'],
                area_acres=str(load.convert_sq_ft_to_acres(int(lot['Lot Area']))),
                centroid_source=lot['point source'],
                centroid=self._get_centroid(lot),

                school_district=lot['School District'],
                council=lot['City Council District'],
                council_district=lot['Community District'],
                police_precinct=lot['Police Precinct'],
            )
            saved_lot.save()

    def backwards(self, orm):
        "Write your backwards methods here."


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lots.alias': {
            'Meta': {'object_name': 'Alias'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lots.Lot']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'lots.lot': {
            'Meta': {'object_name': 'Lot'},
            'accessible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'actual_use': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'area_acres': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '6', 'blank': 'True'}),
            'assess_land': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assess_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'bbl': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'block': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'borough': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'centroid_source': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'council': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'council_district': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'exempt_land': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exempt_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fire_comp': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'group_has_access': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'health_area': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'health_ctr': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_vacant': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lot': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lots.Owner']", 'null': 'True', 'blank': 'True'}),
            'police_precinct': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'polygon': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'qrcode': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'school_district': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'lots.lotgroup': {
            'Meta': {'object_name': 'LotGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lots': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lots.Lot']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'lots.owner': {
            'Meta': {'object_name': 'Owner'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lots.OwnerType']", 'null': 'True', 'blank': 'True'})
        },
        'lots.ownertype': {
            'Meta': {'object_name': 'OwnerType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'lots.review': {
            'Meta': {'object_name': 'Review'},
            'accessible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'actual_use': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hpd_plans': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'hpd_plans_details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'in_use': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lots.Lot']"}),
            'nearby_lots': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'needs_further_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'should_be_imported': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['lots']
