# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration

class Migration(SchemaMigration):

    def forwards(self, orm):
        """
        Add Action.place, which is added using contribute_to_class in 
        activity_stream.models.
        """
        db.add_column(
            'actstream_action',
            'place',
            self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True),
            keep_default=False
        )

    def backwards(self, orm):
        """Remove Action.place"""
        db.delete_column('actstream_action', 'place')

    models = {
        
    }

    complete_apps = ['activity_stream']
