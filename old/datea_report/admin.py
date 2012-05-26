from mptt.admin import MPTTModelAdmin
from django import forms
from django.contrib import admin
from olwidget.admin import GeoModelAdmin
from .models import *

from olwidget.fields import MapField, EditableLayerField
from .forms import ReportAdminForm, ZoneAdminForm, ReportEnvironmentAdminForm
from .widgets import *
from django.contrib.sites.models import Site

from datea_admin.views import get_filtered_reports, get_report_page, get_map_data
from django.utils import simplejson

import logging

class ZoneInline(admin.TabularInline):
    model = Zone
    template = "datea_report/admin/zone_tabular_inline.html"
    exclude=('center',)
    extra = 0
    class Media:
        css = {'all': ('datea/admin/css/zona_tabular_inline.css',)}

class ReportEnvironmentAdmin(GeoModelAdmin):
    form = ReportEnvironmentAdminForm
    inlines = [ZoneInline]
    
    def queryset(self, request):
        qs = super(ReportEnvironmentAdmin, self).queryset(request)
        #if request.user.is_superuser:
        #    return qs
        return qs.filter(sites=Site.objects.get_current())
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "categories":
            kwargs["queryset"] = Category.objects.filter(sites=Site.objects.get_current())
        return super(ReportEnvironmentAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
    
    def change_view(self,request, object_id, extra_context=None):
        env = ReportEnvironment.objects.get(pk=object_id)
        if (env.admin_group in request.user.groups.all()) or request.user.is_staff:
            env_data  = env.build_environment_data()
            env_data_json  = env.get_json_environment()
        
            reports = Report.objects.filter(environment=env).order_by('-created')
        
            inbox_reports = get_filtered_reports({'published': 1, 'status': 'new'}, env, reports)
            page_new = get_report_page(inbox_reports)
            
            map_reports = simplejson.dumps(get_map_data(env, reports.distinct()))
            
            tpl_data = {
                'environment': env,
                'env_data': env_data,
                'env_data_json': env_data_json,
                'reports_page': page_new,
                'map_reports': map_reports,
            }
            return super(ReportEnvironmentAdmin, self).change_view(request, object_id,
            extra_context=tpl_data)    
    
class ZoneAdmin(GeoModelAdmin):
    maps = (
        (('center', 'boundary'), { 'layers': ['google.streets'] }),
    )
    
class VideoInline(admin.TabularInline):
    model=ReportVideo
    extra=1
    max_num=1
    
   
class ReportAdmin(admin.ModelAdmin):
    form = ReportAdminForm
    change_form_template = 'datea_report/admin/report_change_form.html'
    inlines = [VideoInline]
    

    fieldsets = (
              (None, {'fields': ('title','published','author','problem','solution', 'category', 'position', 'street', 'vote_count')}),
                 
              ('Advanced Options', { 
                    'fields': ('site', 'environment'),
                    'classes': ('collapse',)
                    }
                ), 
              )
    readonly_fields = ('vote_count',)
    
    def change_view(self, request, object_id, extra_content=None):
        instance = Report.objects.get(pk=object_id)
        map_context = { 'environment_data': instance.environment.get_json_environment()}
        return super(ReportAdmin, self).change_view(request, object_id, extra_context=map_context)
    
    def queryset(self, request):
        qs = super(ReportAdmin, self).queryset(request)
        #if request.user.is_superuser:
        #    return qs
        return qs.filter(site=Site.objects.get_current())
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "categories":
            kwargs["queryset"] = Category.objects.filter(sites=Site.objects.get_current())
        return super(ReportAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
   

class CategoryAdmin(MPTTModelAdmin):
    model = Category

    def queryset(self, request):
        qs = super(CategoryAdmin, self).queryset(request)
        #if request.user.is_superuser:
        #    return qs
        return qs.filter(sites=Site.objects.get_current())
    
admin.site.register(Report, ReportAdmin)
#admin.site.register(Zone, ZoneAdmin)
admin.site.register(ReportEnvironment, ReportEnvironmentAdmin)
admin.site.register(Category, CategoryAdmin)

