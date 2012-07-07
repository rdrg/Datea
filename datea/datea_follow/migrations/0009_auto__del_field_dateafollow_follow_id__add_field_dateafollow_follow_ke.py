# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'DateaFollow.follow_id'
        db.delete_column('datea_follow_dateafollow', 'follow_id')

        # Adding field 'DateaFollow.follow_key'
        db.add_column('datea_follow_dateafollow', 'follow_key',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Deleting field 'DateaHistory.follow_id'
        db.delete_column('datea_follow_dateahistory', 'follow_id')

        # Deleting field 'DateaHistory.notice_type'
        db.delete_column('datea_follow_dateahistory', 'notice_type')

        # Deleting field 'DateaHistory.history_item_id'
        db.delete_column('datea_follow_dateahistory', 'history_item_id')

        # Adding field 'DateaHistory.history_type'
        db.add_column('datea_follow_dateahistory', 'history_type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'DateaHistory.follow_key'
        db.add_column('datea_follow_dateahistory', 'follow_key',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'DateaHistory.history_key'
        db.add_column('datea_follow_dateahistory', 'history_key',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'DateaFollow.follow_id'
        db.add_column('datea_follow_dateafollow', 'follow_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Deleting field 'DateaFollow.follow_key'
        db.delete_column('datea_follow_dateafollow', 'follow_key')

        # Adding field 'DateaHistory.follow_id'
        db.add_column('datea_follow_dateahistory', 'follow_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'DateaHistory.notice_type'
        db.add_column('datea_follow_dateahistory', 'notice_type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'DateaHistory.history_item_id'
        db.add_column('datea_follow_dateahistory', 'history_item_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Deleting field 'DateaHistory.history_type'
        db.delete_column('datea_follow_dateahistory', 'history_type')

        # Deleting field 'DateaHistory.follow_key'
        db.delete_column('datea_follow_dateahistory', 'follow_key')

        # Deleting field 'DateaHistory.history_key'
        db.delete_column('datea_follow_dateahistory', 'history_key')


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
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'follower_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': "orm['auth.User']"}),
            'user_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
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
        'datea_follow.dateafollow': {
            'Meta': {'object_name': 'DateaFollow'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'follow_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'follows'", 'to': "orm['auth.User']"})
        },
        'datea_follow.dateahistory': {
            'Meta': {'object_name': 'DateaHistory'},
            'acting_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'acting_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'acting_types'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'action': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'notices'", 'null': 'True', 'to': "orm['datea_action.DateaAction']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'extract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'follow_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'history_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'receiver_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'receiver_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'receiver_types'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_notices'", 'to': "orm['auth.User']"})
        },
        'datea_follow.dateanotifysettings': {
            'Meta': {'object_name': 'DateaNotifySettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_comment': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'new_content': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'new_vote': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notice_from_action': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notice_from_site': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'notify_settings'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'datea_image.dateaimage': {
            'Meta': {'object_name': 'DateaImage'},
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['datea_follow']