# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DateaMapItem'
        db.create_table('datea_mapping_dateamapitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='map_items', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=15)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('position', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, spatial_index=False, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.related.ForeignKey')(related_name='map_items', to=orm['datea_mapping.DateaMapping'])),
            ('category', self.gf('mptt.fields.TreeForeignKey')(default=None, related_name='map_items', null=True, blank=True, to=orm['datea_category.DateaFreeCategory'])),
            ('vote_count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('comment_count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('follow_count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('reply_count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('datea_mapping', ['DateaMapItem'])

        # Adding M2M table for field images on 'DateaMapItem'
        db.create_table('datea_mapping_dateamapitem_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dateamapitem', models.ForeignKey(orm['datea_mapping.dateamapitem'], null=False)),
            ('dateaimage', models.ForeignKey(orm['datea_image.dateaimage'], null=False))
        ))
        db.create_unique('datea_mapping_dateamapitem_images', ['dateamapitem_id', 'dateaimage_id'])

        # Adding model 'DateaMapping'
        db.create_table('datea_mapping_dateamapping', (
            ('dateaaction_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['datea_action.DateaAction'], unique=True, primary_key=True)),
            ('mission', self.gf('django.db.models.fields.TextField')(max_length=500, null=True, blank=True)),
            ('information_destiny', self.gf('django.db.models.fields.TextField')(max_length=500)),
            ('long_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('report_success_message', self.gf('django.db.models.fields.TextField')(max_length=140, null=True, blank=True)),
            ('center', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, spatial_index=False, blank=True)),
            ('boundary', self.gf('django.contrib.gis.db.models.fields.PolygonField')(null=True, spatial_index=False, blank=True)),
        ))
        db.send_create_signal('datea_mapping', ['DateaMapping'])

        # Adding M2M table for field item_categories on 'DateaMapping'
        db.create_table('datea_mapping_dateamapping_item_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dateamapping', models.ForeignKey(orm['datea_mapping.dateamapping'], null=False)),
            ('dateafreecategory', models.ForeignKey(orm['datea_category.dateafreecategory'], null=False))
        ))
        db.create_unique('datea_mapping_dateamapping_item_categories', ['dateamapping_id', 'dateafreecategory_id'])


    def backwards(self, orm):
        # Deleting model 'DateaMapItem'
        db.delete_table('datea_mapping_dateamapitem')

        # Removing M2M table for field images on 'DateaMapItem'
        db.delete_table('datea_mapping_dateamapitem_images')

        # Deleting model 'DateaMapping'
        db.delete_table('datea_mapping_dateamapping')

        # Removing M2M table for field item_categories on 'DateaMapping'
        db.delete_table('datea_mapping_dateamapping_item_categories')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'datea_action.dateaaction': {
            'Meta': {'object_name': 'DateaAction'},
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'category': ('mptt.fields.TreeForeignKey', [], {'default': 'None', 'related_name': "'actions'", 'null': 'True', 'blank': 'True', 'to': "orm['datea_category.DateaCategory']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': "orm['auth.User']"})
        },
        'datea_category.dateacategory': {
            'Meta': {'object_name': 'DateaCategory'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'#cccccc'", 'max_length': '7'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'categories_image'", 'null': 'True', 'to': "orm['datea_image.DateaImage']"}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'marker_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'categories_marker'", 'null': 'True', 'to': "orm['datea_image.DateaImage']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['datea_category.DateaCategory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'datea_category.dateafreecategory': {
            'Meta': {'object_name': 'DateaFreeCategory'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'#cccccc'", 'max_length': '7'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'free_categories_image'", 'null': 'True', 'to': "orm['datea_image.DateaImage']"}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'marker_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'free_categories_marker'", 'null': 'True', 'to': "orm['datea_image.DateaImage']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['datea_category.DateaFreeCategory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'datea_image.dateaimage': {
            'Meta': {'object_name': 'DateaImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'datea_mapping.dateamapitem': {
            'Meta': {'object_name': 'DateaMapItem'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'category': ('mptt.fields.TreeForeignKey', [], {'default': 'None', 'related_name': "'map_items'", 'null': 'True', 'blank': 'True', 'to': "orm['datea_category.DateaFreeCategory']"}),
            'comment_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'follow_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'map_item_images'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['datea_image.DateaImage']"}),
            'mapping': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'map_items'", 'to': "orm['datea_mapping.DateaMapping']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'position': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'spatial_index': 'False', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'reply_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '15'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'map_items'", 'to': "orm['auth.User']"}),
            'vote_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'datea_mapping.dateamapping': {
            'Meta': {'object_name': 'DateaMapping', '_ormbases': ['datea_action.DateaAction']},
            'boundary': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'spatial_index': 'False', 'blank': 'True'}),
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'spatial_index': 'False', 'blank': 'True'}),
            'dateaaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['datea_action.DateaAction']", 'unique': 'True', 'primary_key': 'True'}),
            'information_destiny': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'item_categories': ('mptt.fields.TreeManyToManyField', [], {'related_name': "'mappings'", 'default': 'None', 'to': "orm['datea_category.DateaFreeCategory']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mission': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'report_success_message': ('django.db.models.fields.TextField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['datea_mapping']