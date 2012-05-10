# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'FacebookPhotoAccount.facebook_id'
        db.delete_column('photos_facebookphotoaccount', 'facebook_id')

        # Deleting field 'FacebookPhotoAlbum.facebook_id'
        db.delete_column('photos_facebookphotoalbum', 'facebook_id')


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'FacebookPhotoAccount.facebook_id'
        raise RuntimeError("Cannot reverse this migration. 'FacebookPhotoAccount.facebook_id' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'FacebookPhotoAlbum.facebook_id'
        raise RuntimeError("Cannot reverse this migration. 'FacebookPhotoAlbum.facebook_id' and its values cannot be restored.")


    models = {
        'photos.facebookphotoaccount': {
            'Meta': {'object_name': 'FacebookPhotoAccount'},
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'photos.facebookphotoalbum': {
            'Meta': {'object_name': 'FacebookPhotoAlbum'},
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
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
