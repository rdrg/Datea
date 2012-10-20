from tastypie.resources import ModelResource
from tastypie import fields
from api_base import DateaBaseResource, ApiKeyPlusWebAuthentication, DateaBaseAuthorization
from datea.datea_vote.models import DateaVote

class VoteResource(DateaBaseResource):
    
    def hydrate(self,bundle):
        
        if bundle.request.method == 'POST':
            bundle.obj.user = bundle.request.user  
            
        return bundle
    
    class Meta:
        queryset = DateaVote.objects.all()
        resource_name = 'vote'
        allowed_methods = ['get','post','delete']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DateaBaseAuthorization()
        always_return_data = True
