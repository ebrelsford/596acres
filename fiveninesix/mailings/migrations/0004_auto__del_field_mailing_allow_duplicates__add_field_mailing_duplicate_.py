# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Mailing.allow_duplicates'
        db.delete_column('mailings_mailing', 'allow_duplicates')

        # Adding field 'Mailing.duplicate_handling'
        db.add_column('mailings_mailing', 'duplicate_handling', self.gf('django.db.models.fields.CharField')(default='each', max_length=32), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Mailing.allow_duplicates'
        db.add_column('mailings_mailing', 'allow_duplicates', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'Mailing.duplicate_handling'
        db.delete_column('mailings_mailing', 'duplicate_handling')


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
            'duplicate_handling': ('django.db.models.fields.CharField', [], {'default': "'each'", 'max_length': '32'}),
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
