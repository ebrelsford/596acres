# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Lot'
        db.create_table('lots_lot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=256, null=True)),
            ('borough', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('bbl', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('block', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('lot', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lots.Owner'], null=True)),
            ('area', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2)),
            ('centroid', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True)),
            ('polygon', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True)),
        ))
        db.send_create_signal('lots', ['Lot'])

        # Adding model 'Owner'
        db.create_table('lots_owner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lots.OwnerType'], null=True)),
        ))
        db.send_create_signal('lots', ['Owner'])

        # Adding model 'OwnerType'
        db.create_table('lots_ownertype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('lots', ['OwnerType'])


    def backwards(self, orm):
        
        # Deleting model 'Lot'
        db.delete_table('lots_lot')

        # Deleting model 'Owner'
        db.delete_table('lots_owner')

        # Deleting model 'OwnerType'
        db.delete_table('lots_ownertype')


    models = {
        'lots.lot': {
            'Meta': {'object_name': 'Lot'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'bbl': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'block': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'borough': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lot': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lots.Owner']", 'null': 'True'}),
            'polygon': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'})
        },
        'lots.owner': {
            'Meta': {'object_name': 'Owner'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lots.OwnerType']", 'null': 'True'})
        },
        'lots.ownertype': {
            'Meta': {'object_name': 'OwnerType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['lots']
