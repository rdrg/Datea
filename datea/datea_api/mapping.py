from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
#from tastypie.contrib.gis.resources import ModelResource
from datea.datea_mapping.models import DateaMapping, DateaMapItem
from datea.datea_image.models import DateaImage
from datea.datea_category.models import DateaCategory, DateaFreeCategory
from datea.datea_api.category import FreeCategoryResource
from api_base import ApiKeyPlusWebAuthentication, DateaBaseAuthorization, DateaBaseGeoResource
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.utils.text import Truncator


class MappingResource(DateaBaseGeoResource):
    
    user = fields.ToOneField('datea.datea_api.profile.UserResource', 
            attribute='user', full=True, readonly=True)
    item_categories = fields.ToManyField('datea.datea_api.category.FreeCategoryResource', 
            attribute = 'item_categories', full=True, null=True, readonly=True)
    image = fields.ToOneField('datea.datea_api.image.ImageResource', 
            attribute='image', full=True, null=True, readonly=True)
    category = fields.ToOneField('datea.datea_api.category.CategoryResource',
                attribute="category", full=True, null=True, readonly=True)
    
    def dehydrate(self, bundle):
        if bundle.obj.image:
            bundle.data['image_thumb'] = bundle.obj.image.get_thumb('image_thumb_medium')
        else:
            bundle.data['image_thumb']= None
        return bundle
    
    
    def hydrate(self, bundle):
        print "HYDRATING MAPPING!!"
        # save fks by ourselves, tastypie also saves 
        # the related object
        if 'category' in bundle.data and bundle.data['category']:
            bundle.obj.category_id = int(bundle.data['category']) 
    
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


        
class MapItemResource(DateaBaseGeoResource):
    
    category = fields.ToOneField('datea.datea_api.category.FreeCategoryResource',
            attribute= 'category', null=True, full=False, readonly=True)
    images = fields.ToManyField('datea.datea_api.image.ImageResource',
            attribute='images', null=True, full=True, readonly=True)
    mapping = fields.ToOneField('datea.datea_api.mapping.MappingResource',
            attribute='mapping', null=True, full=False, readonly=True)
    user = fields.ToOneField('datea.datea_api.profile.UserResource',
            attribute="user", null=False, full=True, readonly=True)

    def dehydrate(self, bundle):
        bundle.data['category_id'] = bundle.obj.category_id
        bundle.data['category_name'] = bundle.obj.category.name
        bundle.data['category_color'] = bundle.obj.category.color
        bundle.data['extract'] = Truncator( strip_tags(bundle.obj.content) ).chars(140)
        bundle.data['url'] = '/mapping/'+str(bundle.obj.mapping_id)+'/reports/item'+str(bundle.obj.id)
        return bundle
    
    def hydrate(self, bundle):

        bundle.obj.mapping_id = int(bundle.data['mapping'].strip('/').split('/')[-1]) # UGLY HACK -> tatstypie can't find resource by resource uri???
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
        queryset = DateaMapItem.objects.all().order_by('-created')
        resource_name = 'map_item'
        allowed_methods = ['get','post','put','delete']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DateaBaseAuthorization()
        filtering = {
            'mapping': ALL_WITH_RELATIONS,
            'id': ('exact',),
        }


