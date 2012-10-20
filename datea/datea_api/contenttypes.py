from tastypie import fields
from tastypie.resources import ModelResource
from django.contrib.contenttypes.models import ContentType
from tastypie.cache import SimpleCache


class ContentTypeResource(ModelResource):
    
    class Meta:
        queryset = ContentType.objects.all()
        resource_name = 'contenttype'
        allowed_methods = ['get']
        cache = SimpleCache(timeout=100)
        