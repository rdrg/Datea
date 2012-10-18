from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.cache import SimpleCache
from tastypie.throttle import BaseThrottle
#from tastypie.contrib.gis.resources import ModelResource
from datea.datea_mapping.models import DateaMapping, DateaMapItem, DateaMapItemResponse
from datea.datea_image.models import DateaImage
from datea.datea_category.models import DateaCategory, DateaFreeCategory
from datea.datea_api.category import FreeCategoryResource
from api_base import ApiKeyPlusWebAuthentication, DateaBaseAuthorization, DateaBaseGeoResource, DateaBaseResource
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.utils.text import Truncator
from datea.datea_mapping.signals import map_item_response_created, map_item_response_updated
from datea.datea_comment.models import DateaComment


class MappingBaseResource(DateaBaseGeoResource):
    
    user = fields.ToOneField('datea.datea_api.profile.UserResource', 
            attribute='user', full=True, readonly=True)
    item_categories = fields.ToManyField('datea.datea_api.category.FreeCategoryResource', 
            attribute = 'item_categories', full=True, null=True, readonly=True)
    image = fields.ToOneField('datea.datea_api.image.ImageResource', 
            attribute='image', full=True, null=True, readonly=True)
    category = fields.ToOneField('datea.datea_api.category.CategoryResource',
                attribute="category", full=True, null=True, readonly=True)
    
    def dehydrate(self, bundle):
        bundle.data['image_thumb'] = bundle.obj.get_image_thumb('image_thumb_medium')
        bundle.data['url'] = bundle.obj.get_absolute_url()
        return bundle

class MappingResource(MappingBaseResource):
    
    def hydrate(self, bundle):
    # save fks by ourselves, because tastypie also saves 
    # the related object -> we don't want that -> set to readonly
        if 'category' in bundle.data and bundle.data['category']:
            bundle.obj.category_id = int(bundle.data['category']) 
        
        if ( 'image' in bundle.data 
              and bundle.data['image']
              and 'id' in bundle.data['image']):
            bundle.obj.image_id = int(bundle.data['image']['id'])
    
        if bundle.request.method == 'POST':
            # use request user
            bundle.obj.user = bundle.request.user
            
        elif bundle.request.method == 'PUT':
            #preserve owner
            orig_object = DateaMapping.objects.get(pk=bundle.data['id'])
            bundle.obj.user = orig_object.user
    
        return bundle
    
    # do our own saving of related fields,
    # since Tasypie saves those models too! 
    # -> the readonly argument above prevents this 
    # model from saving foreign keys (Why is that the default behavior?!)
    def hydrate_m2m(self,bundle):
        if 'item_categories' in bundle.data and bundle.data['item_categories']:
            cats = [c['id'] for c in bundle.data['item_categories'] if 'id' in c]
            bundle.obj.item_categories = DateaFreeCategory.objects.filter(pk__in=cats)
        return bundle
        
    class Meta:
        queryset = DateaMapping.objects.all()
        resource_name = 'mapping'
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DateaBaseAuthorization()
        cache = SimpleCache(timeout=10)
        limit = 20
        


class MappingFullResource(MappingBaseResource):
    
    map_items = fields.ToManyField('datea.datea_api.mapping.MapItemResource',
                attribute="map_items", full=True, null=True, readonly=True)   
        
    class Meta:
        queryset = DateaMapping.objects.all()
        resource_name = 'mapping_full'
        allowed_methods = ['get']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DateaBaseAuthorization()
        cache = SimpleCache(timeout=10)
        limit = 1

        
class MapItemResource(DateaBaseGeoResource):
    
    category = fields.ToOneField('datea.datea_api.category.FreeCategoryResource',
            attribute= 'category', null=True, full=False, readonly=True)
    images = fields.ToManyField('datea.datea_api.image.ImageResource',
            attribute='images', null=True, full=True, readonly=True)
    action = fields.ToOneField('datea.datea_api.mapping.MappingResource',
            attribute='action', null=True, full=False, readonly=True)
    user = fields.ToOneField('datea.datea_api.profile.UserResource',
            attribute="user", null=False, full=True, readonly=True)
    replies = fields.ToManyField('datea.datea_api.mapping.MapItemResponseResource',
            attribute='responses', null=True, full=True, readonly=True)
    comments = fields.ToManyField('datea.datea_api.comment.CommentResource',
            attribute=lambda bundle: DateaComment.objects.filter(object_id=bundle.obj.id, object_type='dateamapitem'),
            null=True, full=True, readonly=True)

    def dehydrate(self, bundle):
        
        if bundle.obj.category:
            bundle.data['category_id'] = bundle.obj.category_id
            bundle.data['category_name'] = bundle.obj.category.name
            bundle.data['color'] = bundle.obj.category.color
        else:
            bundle.data['color'] = bundle.obj.action.default_color
        
        user_data = {
                     'username': bundle.data['user'].data['username'],
                     'image_small': bundle.data['user'].data['profile'].data['image_small'],
                     'url': bundle.data['user'].data['url'],
                     'resource_uri': bundle.data['user'].data['resource_uri']
                     }
        bundle.data['user'] = user_data
            
        bundle.data['extract'] = Truncator( strip_tags(bundle.obj.content) ).chars(140).replace("\n",' ')
        bundle.data['url'] = bundle.obj.get_absolute_url()
        return bundle
    
    def hydrate(self, bundle):

        bundle.obj.action_id = int(bundle.data['action'].strip('/').split('/')[-1]) # UGLY HACK -> tatstypie can't find resource by resource uri???
        if ( 'category' in bundle.data 
            and bundle.data['category'] 
            and 'id' in bundle.data['category']):
            bundle.obj.category_id = bundle.data['category']['id']
        
        if bundle.request.method == 'POST':
            # use request user
            bundle.obj.user = bundle.request.user
            
        elif bundle.request.method == 'PUT':
            #preserve owner
            orig_object = DateaMapItem.objects.get(pk=bundle.data['id'])
            bundle.obj.user = orig_object.user
        return bundle
    
    
    # do our own saving of related fields (see MappingResource)
    def hydrate_m2m(self, bundle):
        #print bundle.data
        if 'images' in bundle.data and bundle.data['images']:
            imgs = [im['id'] for im in bundle.data['images'] if 'id' in im]
            bundle.obj.images = DateaImage.objects.filter(pk__in=imgs)
        return bundle


    class Meta:
        queryset = DateaMapItem.objects.all()
        resource_name = 'map_item'
        allowed_methods = ['get','post','put','delete']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DateaBaseAuthorization()
        filtering = {
            'action': ALL_WITH_RELATIONS,
            'id': ['exact'],
            'created': ['range', 'gt', 'gte', 'lt', 'lte'],
            'position': ['distance', 'contained','latitude', 'longitude']
        }
        ordering = ['created']
        limit = 500
        cache = SimpleCache(timeout=10)
        
        

class MapItemResponseResource(DateaBaseResource):
    
    user = fields.ToOneField('datea.datea_api.profile.UserResource',
            attribute="user", null=False, full=True, readonly=True)
    map_items = fields.ToManyField('datea.datea_api.mapping.MapItemResource',
            attribute='map_items', null=True, full=False, readonly=True)
    
    def dehydrate(self, bundle):
    
        user_data = {
                     'username': bundle.data['user'].data['username'],
                     'image_small': bundle.data['user'].data['profile'].data['image_small'],
                     'url': bundle.data['user'].data['url'],
                     'resource_uri': bundle.data['user'].data['resource_uri'] 
                     }
        bundle.data['user'] = user_data
        
        return bundle
    
    def hydrate(self, bundle):
        if bundle.request.method == 'POST':
            # use request user
            bundle.obj.user = bundle.request.user
            
        elif bundle.request.method == 'PUT':
            #preserve owner
            orig_object = DateaMapItemResponse.objects.get(pk=bundle.data['id'])
            bundle.obj.user = orig_object.user
        return bundle
    
    # do our own saving of related fields (see MappingResource)
    def hydrate_m2m(self, bundle):
        if 'map_items' in bundle.data and bundle.data['map_items']:
            item_pks = [item['id'] for item in bundle.data['map_items'] if 'id' in item]
            bundle.obj.map_items = DateaMapItem.objects.filter(pk__in=item_pks)
            bundle.obj.method = bundle.request.method
            if bundle.request.method == 'POST':
                map_item_response_created.send(sender=DateaMapItemResponse, instance=bundle.obj)
            elif bundle.request.method == 'PUT':
                map_item_response_updated.send(sender=DateaMapItemResponse, instance=bundle.obj)
        return bundle
    
    
    class Meta:
        queryset = DateaMapItemResponse.objects.all()
        resource_name = 'map_item_response'
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DateaBaseAuthorization()
        ordering = ['created']
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'map_items': ALL_WITH_RELATIONS,
            'id': ['exact'],
            'created': ['range', 'gt', 'gte', 'lt', 'lte'],
        }
        limit = 20
        cache = SimpleCache(timeout=10)
        
