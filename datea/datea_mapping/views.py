# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from svg2png_map_graphics import get_svg_pie_cluster, get_svg_circle
from models import DateaMapping, DateaMapItem
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.text import Truncator
import unicodecsv
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from datetime import datetime
from django.template.defaultfilters import slugify



def get_mapping(request, mapping_id):
    mapping = get_object_or_404(DateaMapping, pk=mapping_id)
    if mapping.image:
        image = mapping.image.image.url
    else:
        image = settings.OPENGRAPH_DEFAULT_IMAGE
        
    return render_to_response("share/og-base.html",{
            'site': Site.objects.get_current(),
            'title': mapping.name,
            'url': mapping.get_absolute_url(),
            'description': mapping.short_description,
            'image': image,
            'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID
            }, context_instance=RequestContext(request))


def get_map_item(request, mapping_id, map_item_id):
    
    map_item = get_object_or_404(DateaMapItem, pk=map_item_id)
    if map_item.images.count() > 0:
        image = map_item.images.all()[0].image.url
    else:
        image = settings.OPENGRAPH_DEFAULT_IMAGE
    
    extract = Truncator( strip_tags(map_item.content) ).chars(140)
    return render_to_response("share/og-base.html",{
            'site': Site.objects.get_current(),
            'title': map_item.user.username+': '+extract[:25]+'...',
            'url': map_item.get_absolute_url(),
            'description': extract,
            'image': image,
            'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID
            }, context_instance=RequestContext(request))


def redirect_to_hash(request, path):    
    return HttpResponseRedirect('/#/mapping/'+path)

def get_pie_cluster(request):
    
    radius = request.GET['radius']
    values = request.GET['values'].split(',')
    colors = request.GET['colors'].split(',')
    
    img_path = get_svg_pie_cluster(radius, values, colors)
    img_data = open(img_path, "rb").read()
    return HttpResponse(img_data, mimetype="image/png")

def get_circle(request):
    radius = request.GET['radius']
    color = request.GET['color']
    img_path = get_svg_circle(radius, color)
    img_data = open(img_path, "rb").read()
    return HttpResponse(img_data, mimetype="image/png")


def csv_export(request, mapping_id):
    
    mapping = DateaMapping.objects.get(id=mapping_id)
    filename = slugify(mapping.name)+'_'+datetime.now().strftime('%d-%m-%Y')
    
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+filename+'.csv"'
    writer = unicodecsv.writer(response, encoding='utf-8')
    
    writer.writerow([_('Username'),_('Created'), _('Category'),_('Content'), _('Status'), _('Images'), _('Latitude'), _('Longitude'), 'URL'])
    
    site = Site.objects.get_current()
    host = 'http://'+site.domain
    
    for item in DateaMapItem.objects.filter(action__id=mapping_id, published=True).order_by('created'):
        
        images = []
        if item.images.count() > 0:
            for img in item.images.all():
                images.append(host+img.image.path)
        images = ','.join(images)
        
        category = ''
        if hasattr(item.category, 'name'):
            category = item.category.name
            
        lat = lng = ''
        if item.position:
            lat = item.position.x
            lng = item.position.y
        
        writer.writerow([
            item.user.username,
            item.created.isoformat(),
            category,
            item.content,
            _(item.status),
            images,
            lat,
            lng,
            host+item.get_absolute_url(),
        ])
        
    return response

