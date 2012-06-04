from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication

from datea.datea_profile.models import DateaProfile

class ProfileResource(ModelResource):
    class Meta:
        queryset = DateaProfile.objects.all()
        resource_name = 'profile/user'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get','post','put', 'delete']
        #TODO: authentication = ApiKeyAuthentication()
        #TODO: authorization = 




