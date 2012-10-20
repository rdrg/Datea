from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import ModelResource, ALL
from datea.datea_category.models import DateaCategory, DateaFreeCategory
from api_base import DateaBaseResource, ApiKeyPlusWebAuthentication, DateaBaseAuthorization
from tastypie.authorization import Authorization


class CategoryResource(ModelResource):
    
    image = fields.ToOneField('datea.datea_api.image.ImageResource',
            attribute='image', full=True, null=True, readonly=True)
    #marker_image = fields.ToOneField('datea.datea_api.image.ImageResource',
    #        attribute='marker_image', full=True, null=True, readonly=True)
    
    def dehydrate(self, bundle):
        #bundle.data['image_thumb'] =  bundle.obj.get_image()
        #bundle.data['marker_image_thumb'] =  bundle.obj.get_marker_image()
        return bundle
    
    def hydrate(self,bundle):
        
        if ( 'image' in bundle.data 
              and bundle.data['image']
              and 'id' in bundle.data['image']):
            bundle.obj.image_id = int(bundle.data['image']['id'])
        
        if ( 'marker_image' in bundle.data 
              and bundle.data['marker_image']
              and 'id' in bundle.data['marker_image']):
            bundle.obj.marker_image_id = int(bundle.data['marker_image']['id'])
        
        if bundle.request.method == 'PUT':
            #preserve original owner
            orig_object = DateaCategory.objects.get(pk=bundle.data['id'])
            bundle.obj.user = orig_object.user 
            
        elif bundle.request.method == 'POST':
            bundle.obj.user = bundle.request.user  
            
        return bundle
     
    class Meta:
        queryset = DateaCategory.objects.all()
        resource_name = 'category'
        allowed_methods = ['get']
  
  
  
#++++++++++++++++++++++  
#  FREE CATEGORIES
     
        
# Base Authorization forFree Categories -> only delete categories without references!!
# derived from http://blog.gingerlime.com/keep-your-hands-off-my-tastypie/
class FreeCategoryAuthorization(Authorization):
    '''
    Per object authorization:
        - read: all allowed
        - update/put: is_staff / object owner
        - delete: is_staff / object owner
    '''
    
    def apply_limits(self, request, object_list=None):
        
        if request and request.method == 'GET':
            return object_list
        
        if request and request.method == 'DELETE':
            return object_list.filter(user=request.user, map_items__exact=None)
 
        if isinstance(object_list, Bundle):
            return object_list # esto hay que implementarlo en cada caso!!!
            
            #if request.method == 'PUT':
            #    print vars(bundle.obj)
            
        return []
    
    
    
class FreeCategoryResource(DateaBaseResource):
    
    image = fields.ToOneField('datea.datea_api.image.ImageResource',
            attribute='image', full=True, null=True, readonly=True)
    marker_image = fields.ToOneField('datea.datea_api.image.ImageResource',
            attribute='marker_image', full=True, null=True, readonly=True)
    
    def dehydrate(self, bundle):
        #bundle.data['image_thumb'] =  bundle.obj.get_image()
        #bundle.data['marker_image_thumb'] =  bundle.obj.get_marker_image()
        return bundle

    def hydrate(self, bundle):
        
        if ( 'image' in bundle.data 
              and bundle.data['image']
              and 'id' in bundle.data['image']):
            bundle.obj.image_id = int(bundle.data['image']['id'])
        
        if ( 'marker_image' in bundle.data 
              and bundle.data['marker_image']
              and 'id' in bundle.data['marker_image']):
            bundle.obj.marker_image_id = int(bundle.data['marker_image']['id'])
        
        if bundle.request.method == 'PUT':
            #preserve original owner
            orig_object = DateaFreeCategory.objects.get(pk=bundle.data['id'])
            bundle.obj.user = orig_object.user 
            
        elif bundle.request.method == 'POST':
            bundle.obj.user = bundle.request.user  
            
        return bundle
    
    
    class Meta:
        queryset = DateaFreeCategory.objects.all()
        resource_name = 'free_category'
        excludes = ['lft', 'rght', 'tree_id']
        filtering={
                'name' : ALL
                }
        allowed_methods = ['get', 'put', 'post', 'delete']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = FreeCategoryAuthorization()
        always_return_data = True
    