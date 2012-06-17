from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from api_base import DateaBaseResource, ApiKeyPlusWebAuthentication, DateaBaseAuthorization
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

from datea.datea_profile.models import DateaProfile

class ProfileResource(DateaBaseResource):
    
    user = fields.ToOneField('datea.datea_api.profile.UserResource',
            attribute = 'user', 
            related_name='profile',
            full=True,
            null=True)
    
    def dehydrate(self, bundle):
        # seeing own profile?
        if bundle.request.user.is_authenticated() and bundle.request.user.pk == bundle.obj.pk:
            bundle.data['is_own'] = True
        # profile image
        bundle.data['image'] = bundle.obj.get_image()
        bundle.data['image_large'] = bundle.obj.get_large_image()
        
        return bundle
    
    def hydrate(self, bundle):
        # leave image foreign keys untouched (must be edited through other methods)
        if 'id' in bundle.data and bundle.data['id']:
            profile = DateaProfile.objects.get(pk=bundle.data['id'])
            bundle.obj.image_social = profile.image_social
            bundle.obj.image = profile.image
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
        exclude = ['image','image_social']
     
       
    # filter own profile with is_own=1
    def obj_get_list(self, request=None, **kwargs):
        
        if hasattr(request, 'GET') and 'is_own' in request.GET:
            if request.user.is_authenticated():
                kwargs.update({'user__id__exact': request.user.pk})
            else:
                kwargs.update({'user__id__exact': 0})
                
        return super(ProfileResource, self).obj_get_list(request, **kwargs)




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
        filtering = {
            'username': ALL,
            'id': ALL,
        }
        



