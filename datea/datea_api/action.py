from tastypie import fields
from tastypie.resources import ModelResource
from datea.datea_action.models import DateaAction
from tastypie.cache import SimpleCache
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from datea.datea_follow.models import DateaFollow

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
        bundle.data['image'] = bundle.obj.get_image_thumb()
        return bundle
    
    def apply_filters(self, request, applicable_filters):
        if hasattr(request, 'GET') and 'following_user' in request.GET:
            action_ids = [f.object_id for f in DateaFollow.objects.filter(object_type='dateaaction', user__id=int(request.GET['following_user']))]
            applicable_filters['id__in'] = action_ids
            
        return super(ActionResource, self).apply_filters(request, applicable_filters)
    
    class Meta:
        queryset = DateaAction.objects.all()
        resource_name = 'action'
        allowed_methods = ['get']
        cache = SimpleCache(timeout=10)
        filtering = {
            'id': ['exact', 'in'],
            'created': ['range', 'gt', 'gte', 'lt', 'lte'],
            'featured': ['exact'],
            'category': ALL_WITH_RELATIONS,
            'user': ALL_WITH_RELATIONS,
            #'position': ['distance', 'contained','latitude', 'longitude']
        }
        