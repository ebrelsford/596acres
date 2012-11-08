# encoding: utf-8
from hashlib import sha1
from south.v2 import DataMigration

from django.conf import settings

class Migration(DataMigration):

    def forwards(self, orm):
        "Give all Organizer objects email hashes."
        for organizer in orm.Organizer.objects.all():
            if organizer.email:
                organizer.email_hash = sha1(settings.PARTICIPANT_SALT + organizer.email).hexdigest()
            organizer.save()

    def backwards(self, orm):
        "Remove all Organizer email hashes"
        orm.Organizer.objects.all().update(email_hash=None)

    models = {
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
            'city_council_district': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'community_district': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'exempt_land': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exempt_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fire_comp': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'group_has_access': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group_with_access': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['organize.Organizer']"}),
            'health_area': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'health_ctr': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_vacant': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lot': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lots.Owner']", 'null': 'True', 'blank': 'True'}),
            'owner_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lots.OwnerContact']", 'null': 'True', 'blank': 'True'}),
            'parent_lot': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['lots.Lot']"}),
            'police_precinct': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'polygon': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'qrcode': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sandy_distribution_site': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sandy_dropoff_site': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'school_district': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'lots.owner': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Owner'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'oasis_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lots.OwnerType']", 'null': 'True', 'blank': 'True'})
        },
        'lots.ownercontact': {
            'Meta': {'ordering': "('name',)", 'object_name': 'OwnerContact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jurisdiction': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lots.Owner']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        'lots.ownertype': {
            'Meta': {'object_name': 'OwnerType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'organize.meeting': {
            'Meta': {'object_name': 'Meeting'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'lots': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lots.Lot']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organize.Organizer']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'organize.note': {
            'Meta': {'object_name': 'Note'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lots.Lot']"}),
            'noter': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'organize.organizer': {
            'Meta': {'object_name': 'Organizer'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'email_hash': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'facebook_page': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lots.Lot']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organize.OrganizerType']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'organize.organizertype': {
            'Meta': {'object_name': 'OrganizerType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'organize.picture': {
            'Meta': {'object_name': 'Picture'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lots.Lot']"}),
            'picture': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'})
        },
        'organize.watcher': {
            'Meta': {'object_name': 'Watcher'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'email_hash': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lots.Lot']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['organize']
