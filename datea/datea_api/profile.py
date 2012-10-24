from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from api_base import DateaBaseResource, ApiKeyPlusWebAuthentication, DateaBaseAuthorization
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from django.conf.urls.defaults import url

from datea.datea_follow.models import DateaFollow
from datea.datea_api.follow import FollowResource
from datea.datea_vote.models import DateaVote
from datea.datea_api.vote import VoteResource

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
        always_return_data = True



class UserResource(DateaBaseResource):
    
    
    profile = fields.ToOneField('datea.datea_api.profile.ProfileResource',
            attribute='profile',
            full=True,
            null=True)
    
    def dehydrate(self, bundle):
        bundle.data['url'] = bundle.obj.profile.get_absolute_url()
        
        # return full user data with follows and casted votes
        
        if hasattr(bundle.request, 'REQUEST') and 'user_full' in bundle.request.REQUEST:
            follows = []
            follow_rsc = FollowResource()
            for f in DateaFollow.objects.filter(user=bundle.obj, published=True):
                f_bundle = follow_rsc.build_bundle(obj=f)
                f_bundle = follow_rsc.full_dehydrate(f_bundle)
                follows.append(f_bundle.data)
            bundle.data['follows'] = follows
            
            votes = []
            vote_rsc = VoteResource()
            for v in DateaVote.objects.filter(user=bundle.obj):
                v_bundle = vote_rsc.build_bundle(obj=v)
                v_bundle = vote_rsc.full_dehydrate(v_bundle)
                votes.append(v_bundle.data)
            bundle.data['votes'] = follows

            if 'api_key' in bundle.request.REQUEST:
                keyauth = ApiKeyAuthentication()
                if keyauth.is_authenticated(bundle.request):
                    if bundle.request.user and bundle.request.user == bundle.obj:
                        bundle.data['email'] = bundle.obj.email
                        print bundle.data
                
        return bundle
    
    def hydrate(self, bundle):
        # clean stuff
        if 'image_small' in bundle.data['profile']:
            del bundle.data['profile']['image_small']
        if 'image' in bundle.data['profile']:
            del bundle.data['profile']['image']
        if 'image_large' in bundle.data['profile']:
            del bundle.data['profile']['image_large']
        
        # keep original object fields not in resource!!! -> not to be changed here
        bundle.obj = User.objects.get(pk=bundle.data['id'])
        # save email
        bundle.obj.email = bundle.data['email']
        return bundle
    
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>[0-9]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
            
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'id','date_joined', 'last_login', 'created']
        filtering = {
                'username':ALL
                }
        allowed_methods = ['get', 'put', 'delete']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DateaBaseAuthorization()
        filtering = {
            'username': ALL,
            'id': ALL,
        }
        always_return_data = True
        



