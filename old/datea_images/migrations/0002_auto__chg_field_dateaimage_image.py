# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'DateaImage.image'
        db.alter_column('datea_images_dateaimage', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=100))


    def backwards(self, orm):
        
        # Changing field 'DateaImage.image'
        db.alter_column('datea_images_dateaimage', 'image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100))


    models = {
        'datea_images.dateaimage': {
            'Meta': {'object_name': 'DateaImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_avatar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['datea_images']
