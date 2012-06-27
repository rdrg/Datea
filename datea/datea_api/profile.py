from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from api_base import DateaBaseResource, ApiKeyPlusWebAuthentication, DateaBaseAuthorization
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

from datea.datea_profile.models import DateaProfile

class ProfileResource(DateaBaseResource):

    #user = fields.ToOneField('datea.datea_api.profile.UserResource',
    #        attribute = 'user', 
    #        related_name='profile',
    #        full=True,
    #        null=True, 
    #        readonly=True)
    
    def dehydrate(self, bundle):
        # profile images
        bundle.data['image_small'] = bundle.obj.get_small_image()
        bundle.data['image'] = bundle.obj.get_image()
        bundle.data['image_large'] = bundle.obj.get_large_image()
        return bundle
    
    def hydrate(self, bundle):
        
        # clean stuff
        if 'image_small' in bundle.data:
            del bundle.data['image_small']
        if 'image' in bundle.data:
            del bundle.data['image']
        if 'image_large' in bundle.data:
            del bundle.data['image_large']
        
        print "PROFILE DATA", bundle.data
        
        # leave image foreign keys to images untouched (must be edited through other methods)
        if 'id' in bundle.data and bundle.data['id']:
            profile = DateaProfile.objects.get(pk=bundle.data['id'])
            bundle.obj.image_social = profile.image_social
            bundle.obj.image = profile.image
            bundle.obj.user = profile.user
        return bundle
    
    class Meta:
        queryset = DateaProfile.objects.all()
        resource_name = 'profile'
        list_allowed_methods = ['get']
        allowed_methods = ['get','post','put', 'delete']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DateaBaseAuthorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
        }
        exclude = ['image','image_social', 'created']



class UserResource(DateaBaseResource):
    
    
    profile = fields.ToOneField('datea.datea_api.profile.ProfileResource',
            attribute='profile',
            full=True,
            null=True)
    
    def hydrate(self, bundle):
         # clean stuff
        if 'image_small' in bundle.data['profile']:
            del bundle.data['profile']['image_small']
        if 'image' in bundle.data['profile']:
            del bundle.data['profile']['image']
        if 'image_large' in bundle.data['profile']:
            del bundle.data['profile']['image_large']
        print "USER DATA", bundle.data
        return bundle
            
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'id','date_joined', 'last_login', 'created']
        filtering = {
                'username':ALL
                }
        allowed_methods = ['get', 'put', 'post','delete']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DateaBaseAuthorization()
        filtering = {
            'username': ALL,
            'id': ALL,
        }
        



