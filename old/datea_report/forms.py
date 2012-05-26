# -*- coding: utf-8 -*-
from django.forms import ModelForm, ModelChoiceField, HiddenInput
from django import forms
from django.forms.models import inlineformset_factory

from models import Report, ReportVideo, ReportEnvironment, Zone
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from sorl.thumbnail.fields import ImageFormField
from widgets import DateaPointLayer

import logging

from olwidget.forms import MapModelForm
from olwidget.fields import MapField, EditableLayerField


class ReportFormBase(MapModelForm):
    
    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    site = forms.ModelChoiceField(queryset=Site.objects.all(), widget=forms.HiddenInput())
    environment = forms.ModelChoiceField(queryset=ReportEnvironment.objects.all(), widget=forms.HiddenInput())
    zone = forms.ModelChoiceField(queryset=Zone.objects.all(), widget=forms.HiddenInput(), required=False)
    

class ReportFormInsideEnv(ReportFormBase):
    
    problem = forms.CharField(
                              widget=forms.Textarea(attrs={'class':'autoresize required text large', 'rows': '1'}),
                              label=u"Descripción del problema",
                              required=True,
                              )
    solution = forms.CharField(
                               widget=forms.Textarea(attrs={'class':'autoresize required text large', 'rows': '1'}),
                               label=u"Propón una solución al problema",
                               required=True,
                               )
    location_description = forms.CharField(
                               widget=forms.Textarea(attrs={'class':'autoresize text large', 'rows': '1'}),
                               label=u"descripción de la ubicación (opcional)",
                               required=False
                               )
    
    status = forms.CharField(required=False)
    
    
    position = MapField(
            fields=[EditableLayerField({'geometry': 'point', 'name': 'position'}, widget=DateaPointLayer())],
            template="datea_report/olwidget/dateapoint_layer_map_inside_env.html" 
        )
    
    class Meta:
        model = Report
        exclude = ('title','reviewed','published')
            
    class Media:
        js = ('datea/olwidget/js/datea_report_pointfield.js',
              'datea/olwidget/js/datea_new_report_map_inside_env.js',
              )
        css = {
               'all': ('datea/olwidget/css/dateapoint_map.css',
                       )
               }
        
        

class ReportFormStandalone(ReportFormBase):
    
    position = MapField(
                        fields=[EditableLayerField({'geometry': 'point', 'name': 'position'}, widget=DateaPointLayer())],
                        options={
                         'overlay_style': {
                                  'externalGraphic': '/site_media/static/openlayers/img/marker.png', 
                                  'graphicHeight': 21, 
                                  'graphicWidth': 16,
                                  'graphic_opacity': 1         
                            }
                        },
                        template="datea_report/olwidget/dateapoint_layer_map.html" 
                )
    
    class Meta:
        model = Report
        exclude = ('reviewed','published')
        #options = { 'layers': ['google.streets'] }
        
    class Media:
        js = ('datea/olwidget/js/datea_report_pointfield.js',
              )
        css = {
               'all': ('datea/olwidget/css/dateapoint_map.css',
                       )
               }
        

class ReportEnvAdminForm(ReportFormBase):
    '''
    problem = forms.CharField(
                              widget=forms.Textarea(attrs={'class':'autoresize required text large', 'rows': '1'}),
                              label=u"Descripción del problema",
                              required=True,
                              )
    solution = forms.CharField(
                               widget=forms.Textarea(attrs={'class':'autoresize required text large', 'rows': '1'}),
                               label=u"Propón una solución al problema",
                               required=True,
                               )
    location_description = forms.CharField(
                               widget=forms.Textarea(attrs={'class':'autoresize text large', 'rows': '1'}),
                               label=u"descripción de la ubicación (opcional)",
                               required=False
                               )
    '''
    problem = forms.CharField(widget=forms.HiddenInput())
    solution = forms.CharField(widget=forms.HiddenInput())
    location_description = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Report
        exclude = ('street', 'vote_count', 'reply_count', 'follow_count', 'comment_count', 'title')
    
        
class ReportAdminForm(ModelForm):
    
    position = MapField(
                    fields=[EditableLayerField({'geometry': 'point', 'name': 'position'}, widget=DateaPointLayer())],
                    options={
                     'overlay_style': {
                              'externalGraphic': '/site_media/static/openlayers/img/marker.png', 
                              'graphicHeight': 21, 
                              'graphicWidth': 16,
                              'graphic_opacity': 1         
                        },
                    },
                    template="datea_report/olwidget/dateapoint_layer_map_admin.html", 
            )

    class Meta:
        model = Report
        exclude = ('reviewed',)
        #options = { 'layers': ['google.streets'] }
        
    class Media:
        js = ('datea/olwidget/js/datea_report_pointfield.js',)
        css = {
               'all': ('datea/olwidget/css/dateapoint_map.css',)
               }
        
ReportVideoFormSet = inlineformset_factory(Report, ReportVideo, max_num=1)


# ZONE FORM FOR ADMIN
class ZoneAdminForm(ModelForm):
    
    boundary = MapField(fields=[EditableLayerField({'geometry': 'polygon', 'name': 'boundary'})])
    
    class Meta:
        exclude=('center',)
        model = Zone
        maps = (
            (('center', 'boundary'), { 'layers': ['google.streets'] }),
        )
        
class ReportEnvironmentAdminForm(ModelForm):
    
    boundary = MapField(fields=[EditableLayerField({'geometry': 'polygon', 'name': 'boundary'})],
                        template="datea_report/olwidget/reportenvironment_admin_map.html",
                        options={
                            'layers': ['google.streets', 'google.hybrid', 'osm.mapnik'],
                            'map_div_style': {'width': '850px', 'height': '600px'}
                        }
                    )
    class Meta:
        model=ReportEnvironment
        
    class Media:
        js = ('datea/admin/js/datea_utils.js',
              'datea/olwidget/js/environment_admin_map.js',
              )

