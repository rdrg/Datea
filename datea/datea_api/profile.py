from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from api_base import DateaBaseResource, ApiKeyPlusWebAuthentication, DateaBaseAuthorization

from datea.datea_profile.models import DateaProfile

class ProfileResource(DateaBaseResource):
    user = fields.ToOneField('datea.datea_api.profile.UserResource',
            attribute = 'user', 
            related_name='profile',
            full=True,
            null=True)
    
    class Meta:
        queryset = DateaProfile.objects.all()
        resource_name = 'profile'
        #list_allowed_methods = ['get']
        allowed_methods = ['get','post','put', 'delete']
        authentication = ApiKeyAuthentication()
        authorization = DateaBaseAuthorization()



class UserResource(DateaBaseResource):
   class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'id','date_joined', 'last_login']
        filtering = {
                'username':ALL
                }
        allowed_methods = ['get', 'put', 'post','delete']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DateaBaseAuthorization()




