# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ContactRequest'
        db.create_table('contact_contactrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('handled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('contact', ['ContactRequest'])


    def backwards(self, orm):
        
        # Deleting model 'ContactRequest'
        db.delete_table('contact_contactrequest')


    models = {
        'contact.contactrequest': {
            'Meta': {'object_name': 'ContactRequest'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'handled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        'contact.joinusrequest': {
            'Meta': {'object_name': 'JoinUsRequest'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
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
