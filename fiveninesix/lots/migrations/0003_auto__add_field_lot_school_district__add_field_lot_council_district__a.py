# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Lot.school_district'
        db.add_column('lots_lot', 'school_district', self.gf('django.db.models.fields.CharField')(max_length=16, null=True), keep_default=False)

        # Adding field 'Lot.council_district'
        db.add_column('lots_lot', 'council_district', self.gf('django.db.models.fields.CharField')(max_length=16, null=True), keep_default=False)

        # Adding field 'Lot.council'
        db.add_column('lots_lot', 'council', self.gf('django.db.models.fields.CharField')(max_length=16, null=True), keep_default=False)

        # Adding field 'Lot.fire_comp'
        db.add_column('lots_lot', 'fire_comp', self.gf('django.db.models.fields.CharField')(max_length=16, null=True), keep_default=False)

        # Adding field 'Lot.health_area'
        db.add_column('lots_lot', 'health_area', self.gf('django.db.models.fields.CharField')(max_length=16, null=True), keep_default=False)

        # Adding field 'Lot.health_ctr'
        db.add_column('lots_lot', 'health_ctr', self.gf('django.db.models.fields.CharField')(max_length=16, null=True), keep_default=False)

        # Adding field 'Lot.police_precinct'
        db.add_column('lots_lot', 'police_precinct', self.gf('django.db.models.fields.CharField')(max_length=16, null=True), keep_default=False)

        # Adding field 'Lot.assess_land'
        db.add_column('lots_lot', 'assess_land', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)

        # Adding field 'Lot.assess_total'
        db.add_column('lots_lot', 'assess_total', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)

        # Adding field 'Lot.exempt_land'
        db.add_column('lots_lot', 'exempt_land', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)

        # Adding field 'Lot.exempt_total'
        db.add_column('lots_lot', 'exempt_total', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Lot.school_district'
        db.delete_column('lots_lot', 'school_district')

        # Deleting field 'Lot.council_district'
        db.delete_column('lots_lot', 'council_district')

        # Deleting field 'Lot.council'
        db.delete_column('lots_lot', 'council')

        # Deleting field 'Lot.fire_comp'
        db.delete_column('lots_lot', 'fire_comp')

        # Deleting field 'Lot.health_area'
        db.delete_column('lots_lot', 'health_area')

        # Deleting field 'Lot.health_ctr'
        db.delete_column('lots_lot', 'health_ctr')

        # Deleting field 'Lot.police_precinct'
        db.delete_column('lots_lot', 'police_precinct')

        # Deleting field 'Lot.assess_land'
        db.delete_column('lots_lot', 'assess_land')

        # Deleting field 'Lot.assess_total'
        db.delete_column('lots_lot', 'assess_total')

        # Deleting field 'Lot.exempt_land'
        db.delete_column('lots_lot', 'exempt_land')

        # Deleting field 'Lot.exempt_total'
        db.delete_column('lots_lot', 'exempt_total')


    models = {
        'lots.lot': {
            'Meta': {'object_name': 'Lot'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'assess_land': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'assess_total': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'bbl': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'block': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'borough': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'council': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'council_district': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'exempt_land': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'exempt_total': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'fire_comp': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'health_area': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'health_ctr': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lot': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lots.Owner']", 'null': 'True'}),
            'police_precinct': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'polygon': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'school_district': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'})
        },
        'lots.owner': {
            'Meta': {'object_name': 'Owner'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'}),
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
