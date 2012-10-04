# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SizeComparable'
        db.create_table('sizecompare_sizecomparable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('sqft', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('sizecompare', ['SizeComparable'])


    def backwards(self, orm):
        
        # Deleting model 'SizeComparable'
        db.delete_table('sizecompare_sizecomparable')


    models = {
        'sizecompare.sizecomparable': {
            'Meta': {'object_name': 'SizeComparable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'sqft': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['sizecompare']
