from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from datea.datea_follow.models import DateaFollow, DateaHistory, DateaNotifySettings
from api_base import DateaBaseResource, ApiKeyPlusWebAuthentication, DateaBaseAuthorization


class FollowResource(DateaBaseResource):
    
    user = fields.ToOneField('datea.datea_api.profile.UserResource', 
            attribute='user', full=True, readonly=True)
    
    def hydrate(self,bundle):
        
        if bundle.request.method == 'PUT':
            #preserve original owner
            orig_object = DateaFollow.objects.get(pk=bundle.data['id'])
            bundle.obj.user = orig_object.user 
            
        elif bundle.request.method == 'POST':
            bundle.obj.user = bundle.request.user  
            
        return bundle
     
     
    class Meta:
        queryset = DateaFollow.objects.all()
        resource_name = 'follow'
        allowed_methods = ['get', 'post', 'put', 'delete']
        filtering={
                'id' : ['exact'],
                'user': ALL_WITH_RELATIONS,
                'object_type': ['exact'],
                'object_id': ['exact']
                }
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DateaBaseAuthorization()
        limit = 50
        
        
class HistoryResource(DateaBaseResource):
    
    class Meta:
        queryset= DateaHistory.objects.all()
        resource_name= 'history'
        filtering = {
                     'id': ['exact'],
                     'user': ALL_WITH_RELATIONS,
                     'action': ALL_WITH_RELATIONS,
                     'object_type': ['exact'],
                     'object_id': ['exact'],
                     'follow_id': ['exact'],
                     'history_id': ['exact'],
                     }
    
        