from tastypie import fields
from tastypie.resources import ModelResource
from datea.datea_action.models import DateaAction
from tastypie.cache import SimpleCache
from tastypie.constants import ALL, ALL_WITH_RELATIONS

class ActionResource(ModelResource):
    
    user = fields.ToOneField('datea.datea_api.profile.UserResource',
            attribute="user", null=False, full=False, readonly=True)
    category = fields.ToOneField('datea.datea_api.category.CategoryResource',
            attribute='category', null=True, full=True, readonly=True)
    #image = fields.ToOneField('datea.datea_api.image.ImageResource', 
    #        attribute='image', full=True, null=True, readonly=True)
    
    def dehydrate(self, bundle):
        bundle.data['url'] = bundle.obj.get_absolute_url()
        bundle.data['type'] = bundle.obj.action_type
        bundle.data['image'] = bundle.obj.image.get_thumb('action_image')
        return bundle
    
    class Meta:
        queryset = DateaAction.objects.all()
        resource_name = 'action'
        allowed_methods = ['get']
        cache = SimpleCache(timeout=10)
        filtering = {
            'id': ['exact', 'in'],
            'created': ['range', 'gt', 'gte', 'lt', 'lte'],
            'featured': ['exact'],
            'category': ALL_WITH_RELATIONS
            #'position': ['distance', 'contained','latitude', 'longitude']
        }