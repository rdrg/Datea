from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from datea.datea_comment.models import DateaComment
from api_base import DateaBaseResource, ApiKeyPlusWebAuthentication, DateaBaseAuthorization
from tastypie.authorization import Authorization
from django.template.defaultfilters import linebreaksbr


class CommentResource(DateaBaseResource):
    
    user = fields.ToOneField('datea.datea_api.profile.UserResource', 
            attribute='user', full=True, readonly=True)
    
    def hydrate(self,bundle):
        
        if bundle.request.method == 'PUT':
            #preserve original owner
            orig_object = DateaComment.objects.get(pk=bundle.data['id'])
            bundle.obj.user = orig_object.user 
            
        elif bundle.request.method == 'POST':
            bundle.obj.user = bundle.request.user  
            
        return bundle
     
     
    class Meta:
        queryset = DateaComment.objects.all()
        resource_name = 'comment'
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
        ordering=['created']
        
        