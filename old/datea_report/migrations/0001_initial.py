# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Report'
        db.create_table('datea_report_report', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('reviewed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('position', self.gf('geoposition.fields.GeopositionField')(default='', max_length=42, blank=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['datea_report.Zone'], null=True, blank=True)),
            ('category', self.gf('mptt.fields.TreeForeignKey')(default=None, to=orm['datea_report.Category'], null=True, blank=True)),
            ('environment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datea_report.ReportEnvironment'])),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('datea_report', ['Report'])

        # Adding model 'ReportImage'
        db.create_table('datea_report_reportimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Images', to=orm['datea_report.Report'])),
        ))
        db.send_create_signal('datea_report', ['ReportImage'])

        # Adding model 'ReportVideo'
        db.create_table('datea_report_reportvideo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Video', to=orm['datea_report.Report'])),
        ))
        db.send_create_signal('datea_report', ['ReportVideo'])

        # Adding model 'Zone'
        db.create_table('datea_report_zone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('center', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, spatial_index=False, blank=True)),
            ('boundary', self.gf('django.contrib.gis.db.models.fields.PolygonField')()),
        ))
        db.send_create_signal('datea_report', ['Zone'])

        # Adding M2M table for field sites on 'Zone'
        db.create_table('datea_report_zone_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('zone', models.ForeignKey(orm['datea_report.zone'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('datea_report_zone_sites', ['zone_id', 'site_id'])

        # Adding model 'Category'
        db.create_table('datea_report_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=500)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['datea_report.Category'])),
            ('color', self.gf('django.db.models.fields.CharField')(default='#cccccc', max_length=7)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('marker_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('datea_report', ['Category'])

        # Adding M2M table for field sites on 'Category'
        db.create_table('datea_report_category_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm['datea_report.category'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('datea_report_category_sites', ['category_id', 'site_id'])

        # Adding model 'ReportEnvironment'
        db.create_table('datea_report_reportenvironment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=15, db_index=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('center', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, spatial_index=False, blank=True)),
            ('boundary', self.gf('django.contrib.gis.db.models.fields.PolygonField')(null=True, spatial_index=False, blank=True)),
        ))
        db.send_create_signal('datea_report', ['ReportEnvironment'])

        # Adding M2M table for field zones on 'ReportEnvironment'
        db.create_table('datea_report_reportenvironment_zones', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reportenvironment', models.ForeignKey(orm['datea_report.reportenvironment'], null=False)),
            ('zone', models.ForeignKey(orm['datea_report.zone'], null=False))
        ))
        db.create_unique('datea_report_reportenvironment_zones', ['reportenvironment_id', 'zone_id'])

        # Adding M2M table for field sites on 'ReportEnvironment'
        db.create_table('datea_report_reportenvironment_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reportenvironment', models.ForeignKey(orm['datea_report.reportenvironment'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('datea_report_reportenvironment_sites', ['reportenvironment_id', 'site_id'])


    def backwards(self, orm):
        
        # Deleting model 'Report'
        db.delete_table('datea_report_report')

        # Deleting model 'ReportImage'
        db.delete_table('datea_report_reportimage')

        # Deleting model 'ReportVideo'
        db.delete_table('datea_report_reportvideo')

        # Deleting model 'Zone'
        db.delete_table('datea_report_zone')

        # Removing M2M table for field sites on 'Zone'
        db.delete_table('datea_report_zone_sites')

        # Deleting model 'Category'
        db.delete_table('datea_report_category')

        # Removing M2M table for field sites on 'Category'
        db.delete_table('datea_report_category_sites')

        # Deleting model 'ReportEnvironment'
        db.delete_table('datea_report_reportenvironment')

        # Removing M2M table for field zones on 'ReportEnvironment'
        db.delete_table('datea_report_reportenvironment_zones')

        # Removing M2M table for field sites on 'ReportEnvironment'
        db.delete_table('datea_report_reportenvironment_sites')


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
        'datea_report.category': {
            'Meta': {'object_name': 'Category'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'#cccccc'", 'max_length': '7'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'marker_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['datea_report.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'datea_report.report': {
            'Meta': {'object_name': 'Report'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'category': ('mptt.fields.TreeForeignKey', [], {'default': 'None', 'to': "orm['datea_report.Category']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'environment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datea_report.ReportEnvironment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'position': ('geoposition.fields.GeopositionField', [], {'default': "''", 'max_length': '42', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'reviewed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['datea_report.Zone']", 'null': 'True', 'blank': 'True'})
        },
        'datea_report.reportenvironment': {
            'Meta': {'object_name': 'ReportEnvironment'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'boundary': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'spatial_index': 'False', 'blank': 'True'}),
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'spatial_index': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '15', 'db_index': 'True'}),
            'zones': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['datea_report.Zone']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'})
        },
        'datea_report.reportimage': {
            'Meta': {'object_name': 'ReportImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'original_image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Images'", 'to': "orm['datea_report.Report']"})
        },
        'datea_report.reportvideo': {
            'Meta': {'object_name': 'ReportVideo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Video'", 'to': "orm['datea_report.Report']"}),
            'video': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'datea_report.zone': {
            'Meta': {'object_name': 'Zone'},
            'boundary': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'spatial_index': 'False', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['datea_report']
