from tastypie import fields
from tastypie.resources import ModelResource
from django.contrib.contenttypes.models import ContentType

class ContentTypeResource(ModelResource):
    class Meta:
        queryset = ContentType.objects.all()
        resource_name = 'contenttype'
        allowed_methods = ['get','post','put','delete']
