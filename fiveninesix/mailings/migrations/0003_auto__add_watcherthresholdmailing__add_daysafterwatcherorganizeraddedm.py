# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'WatcherThresholdMailing'
        db.create_table('mailings_watcherthresholdmailing', (
            ('mailing_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mailings.Mailing'], unique=True, primary_key=True)),
            ('number_of_watchers', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('mailings', ['WatcherThresholdMailing'])

        # Adding model 'DaysAfterWatcherOrganizerAddedMailing'
        db.create_table('mailings_daysafterwatcherorganizeraddedmailing', (
            ('daysafteraddedmailing_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mailings.DaysAfterAddedMailing'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('mailings', ['DaysAfterWatcherOrganizerAddedMailing'])


    def backwards(self, orm):
        
        # Deleting model 'WatcherThresholdMailing'
        db.delete_table('mailings_watcherthresholdmailing')

        # Deleting model 'DaysAfterWatcherOrganizerAddedMailing'
        db.delete_table('mailings_daysafterwatcherorganizeraddedmailing')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mailings.daysafteraddedmailing': {
            'Meta': {'object_name': 'DaysAfterAddedMailing', '_ormbases': ['mailings.Mailing']},
            'days_after_added': ('django.db.models.fields.IntegerField', [], {}),
            'mailing_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mailings.Mailing']", 'unique': 'True', 'primary_key': 'True'})
        },
        'mailings.daysafterwatcherorganizeraddedmailing': {
            'Meta': {'object_name': 'DaysAfterWatcherOrganizerAddedMailing', '_ormbases': ['mailings.DaysAfterAddedMailing']},
            'daysafteraddedmailing_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mailings.DaysAfterAddedMailing']", 'unique': 'True', 'primary_key': 'True'})
        },
        'mailings.deliveryrecord': {
            'Meta': {'object_name': 'DeliveryRecord'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailing': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailings.Mailing']"}),
            'receiver_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'receiver_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'recorded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'mailings.mailing': {
            'Meta': {'object_name': 'Mailing'},
            'allow_duplicates': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subject_template_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'target_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['contenttypes.ContentType']", 'symmetrical': 'False'}),
            'text_template_name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'mailings.watcherthresholdmailing': {
            'Meta': {'object_name': 'WatcherThresholdMailing', '_ormbases': ['mailings.Mailing']},
            'mailing_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mailings.Mailing']", 'unique': 'True', 'primary_key': 'True'}),
            'number_of_watchers': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['mailings']
