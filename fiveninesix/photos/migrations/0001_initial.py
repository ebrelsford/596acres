# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FacebookPhotoAccount'
        db.create_table('photos_facebookphotoaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('last_checked', self.gf('django.db.models.fields.DateTimeField')()),
            ('facebook_id', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('photos', ['FacebookPhotoAccount'])

        # Adding model 'FacebookPhotoAlbum'
        db.create_table('photos_facebookphotoalbum', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('last_checked', self.gf('django.db.models.fields.DateTimeField')()),
            ('facebook_id', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('photos', ['FacebookPhotoAlbum'])

        # Adding model 'PhotoAlbum'
        db.create_table('photos_photoalbum', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('external_source', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('external_url', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal('photos', ['PhotoAlbum'])

        # Adding model 'Photo'
        db.create_table('photos_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.PhotoAlbum'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('external_url', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('picture', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
        ))
        db.send_create_signal('photos', ['Photo'])


    def backwards(self, orm):
        
        # Deleting model 'FacebookPhotoAccount'
        db.delete_table('photos_facebookphotoaccount')

        # Deleting model 'FacebookPhotoAlbum'
        db.delete_table('photos_facebookphotoalbum')

        # Deleting model 'PhotoAlbum'
        db.delete_table('photos_photoalbum')

        # Deleting model 'Photo'
        db.delete_table('photos_photo')


    models = {
        'photos.facebookphotoaccount': {
            'Meta': {'object_name': 'FacebookPhotoAccount'},
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'photos.facebookphotoalbum': {
            'Meta': {'object_name': 'FacebookPhotoAlbum'},
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'photos.photo': {
            'Meta': {'object_name': 'Photo'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['photos.PhotoAlbum']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'external_url': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'picture': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'})
        },
        'photos.photoalbum': {
            'Meta': {'object_name': 'PhotoAlbum'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'external_source': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'external_url': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['photos']
