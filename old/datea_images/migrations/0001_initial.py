# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DateaImage'
        db.create_table('datea_images_dateaimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_avatar', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('datea_images', ['DateaImage'])


    def backwards(self, orm):
        
        # Deleting model 'DateaImage'
        db.delete_table('datea_images_dateaimage')


    models = {
        'datea_images.dateaimage': {
            'Meta': {'object_name': 'DateaImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'is_avatar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['datea_images']
