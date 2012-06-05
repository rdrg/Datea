from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication

from datea.datea_profile.models import DateaProfile

class ProfileResource(ModelResource):
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
        #TODO: authentication = ApiKeyAuthentication()
        #TODO: authorization = 

class UserResource(ModelResource):
   class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        #fields = ['username']
        filtering = {
                'username':ALL
                }




