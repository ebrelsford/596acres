# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'GoogleCalendar.magic_cookie'
        db.delete_column('events_googlecalendar', 'magic_cookie')

        # Adding field 'GoogleCalendar.external_id'
        db.add_column('events_googlecalendar', 'external_id', self.gf('django.db.models.fields.CharField')(default='', max_length=256), keep_default=False)

        # Adding field 'GoogleCalendar.token_file'
        db.add_column('events_googlecalendar', 'token_file', self.gf('django.db.models.fields.CharField')(default='', max_length=512), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'GoogleCalendar.magic_cookie'
        db.add_column('events_googlecalendar', 'magic_cookie', self.gf('django.db.models.fields.CharField')(default='', max_length=256), keep_default=False)

        # Deleting field 'GoogleCalendar.external_id'
        db.delete_column('events_googlecalendar', 'external_id')

        # Deleting field 'GoogleCalendar.token_file'
        db.delete_column('events_googlecalendar', 'token_file')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'calendar_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'calendar_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'events.googlecalendar': {
            'Meta': {'object_name': 'GoogleCalendar'},
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'token_file': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['events']
