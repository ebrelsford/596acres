# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'OrganizerType'
        db.create_table('organize_organizertype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('is_group', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('organize', ['OrganizerType'])

        # Adding model 'Meeting'
        db.create_table('organize_meeting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('organizer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organize.Organizer'])),
        ))
        db.send_create_signal('organize', ['Meeting'])

        # Adding M2M table for field lots on 'Meeting'
        db.create_table('organize_meeting_lots', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meeting', models.ForeignKey(orm['organize.meeting'], null=False)),
            ('lot', models.ForeignKey(orm['lots.lot'], null=False))
        ))
        db.create_unique('organize_meeting_lots', ['meeting_id', 'lot_id'])

        # Adding field 'Organizer.type'
        db.add_column('organize_organizer', 'type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['organize.OrganizerType']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'OrganizerType'
        db.delete_table('organize_organizertype')

        # Deleting model 'Meeting'
        db.delete_table('organize_meeting')

        # Removing M2M table for field lots on 'Meeting'
        db.delete_table('organize_meeting_lots')

        # Deleting field 'Organizer.type'
        db.delete_column('organize_organizer', 'type_id')


    models = {
        'lots.lot': {
            'Meta': {'object_name': 'Lot'},
            'actual_use': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'assess_land': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assess_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'bbl': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lots': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lots.Lot']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
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
