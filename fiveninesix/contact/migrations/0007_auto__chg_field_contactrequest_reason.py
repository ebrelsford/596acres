# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        orm.ContactRequest.objects.update(reason='other')
        
        # Changing field 'ContactRequest.reason'
        db.alter_column('contact_contactrequest', 'reason', self.gf('django.db.models.fields.CharField')(max_length=32))


    def backwards(self, orm):
        
        # Changing field 'ContactRequest.reason'
        db.alter_column('contact_contactrequest', 'reason', self.gf('django.db.models.fields.CharField')(max_length=32, null=True))


    models = {
        'contact.contactrequest': {
            'Meta': {'object_name': 'ContactRequest'},
            'borough': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'handled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'default': "'other'", 'max_length': '32'})
        },
        'contact.lotinformationrequest': {
            'Meta': {'object_name': 'LotInformationRequest'},
            'borough': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
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
