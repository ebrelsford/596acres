# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'LotInformationRequest'
        db.create_table('contact_lotinformationrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.TextField')()),
            ('story', self.gf('django.db.models.fields.TextField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('handled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('contact', ['LotInformationRequest'])

        # Adding model 'JoinUsRequest'
        db.create_table('contact_joinusrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('handled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('contact', ['JoinUsRequest'])


    def backwards(self, orm):
        
        # Deleting model 'LotInformationRequest'
        db.delete_table('contact_lotinformationrequest')

        # Deleting model 'JoinUsRequest'
        db.delete_table('contact_joinusrequest')


    models = {
        'contact.joinusrequest': {
            'Meta': {'object_name': 'JoinUsRequest'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'handled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'contact.lotinformationrequest': {
            'Meta': {'object_name': 'LotInformationRequest'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'handled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'story': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['contact']
