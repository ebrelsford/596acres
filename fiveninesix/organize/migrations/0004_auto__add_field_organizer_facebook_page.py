# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Organizer.facebook_page'
        db.add_column('organize_organizer', 'facebook_page', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Organizer.facebook_page'
        db.delete_column('organize_organizer', 'facebook_page')


    models = {
        'lots.lot': {
            'Meta': {'object_name': 'Lot'},
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
        'organize.organizer': {
            'Meta': {'object_name': 'Organizer'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'facebook_page': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lots': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lots.Lot']", 'symmetrical': 'False'}),
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
        }
    }

    complete_apps = ['organize']
