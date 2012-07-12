# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Mailing'
        db.create_table('mailings_mailing', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('allow_duplicates', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('subject_template_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('text_template_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('mailings', ['Mailing'])

        # Adding M2M table for field target_types on 'Mailing'
        db.create_table('mailings_mailing_target_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mailing', models.ForeignKey(orm['mailings.mailing'], null=False)),
            ('contenttype', models.ForeignKey(orm['contenttypes.contenttype'], null=False))
        ))
        db.create_unique('mailings_mailing_target_types', ['mailing_id', 'contenttype_id'])

        # Adding model 'DaysAfterAddedMailing'
        db.create_table('mailings_daysafteraddedmailing', (
            ('mailing_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mailings.Mailing'], unique=True, primary_key=True)),
            ('days_after_added', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('mailings', ['DaysAfterAddedMailing'])

        # Adding model 'DeliveryRecord'
        db.create_table('mailings_deliveryrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('recorded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('mailing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailings.Mailing'])),
            ('receiver_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('receiver_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('mailings', ['DeliveryRecord'])


    def backwards(self, orm):
        
        # Deleting model 'Mailing'
        db.delete_table('mailings_mailing')

        # Removing M2M table for field target_types on 'Mailing'
        db.delete_table('mailings_mailing_target_types')

        # Deleting model 'DaysAfterAddedMailing'
        db.delete_table('mailings_daysafteraddedmailing')

        # Deleting model 'DeliveryRecord'
        db.delete_table('mailings_deliveryrecord')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subject_template_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'target_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['contenttypes.ContentType']", 'symmetrical': 'False'}),
            'text_template_name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['mailings']
