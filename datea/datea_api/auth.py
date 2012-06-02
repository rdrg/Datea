from django.conf.urls.defaults import url 
from django.contrib.auth.models import User
from django.utils import simplejson
from django.contrib.auth import authenticate

from tastypie.resources import ModelResource 
from tastypie.utils import trailing_slash 

from oauth2 import Client as OAuthClient, Consumer as OAuthConsumer, Token
from datea.settings import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
from social_auth.backends.twitter import TWITTER_CHECK_AUTH
from social_auth.models import UserSocialAuth

from utils import getOrCreateKey
from status_codes import *
from datea.datea_profile.utils import make_social_username

class Auth(ModelResource):

    class Meta:
        list_allowed_methods = ['post']

    def override_urls(self):
        return [url(r"^(?P<resource_name>%s)/signin%s$" %
            (self._meta.resource_name, trailing_slash()), 
            self.wrap_view('signin'), name="api_signin"), 
            ]

    def signin(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        
        postData = simplejson.loads(request.raw_post_data)
        username = postData['username']
        password = postData['password']

        user = authenticate(username= username,
                            password= password)

        if user is not None:
            if user.is_active:
                key = getOrCreateKey(user)
                return self.create_response(request,{'status':OK,
                                                    'token': key})
            else:
                return self.create_response(request,{'status':FORBIDDEN,
                                                    'error': 'Account disabled'})
        else:
            return self.create_response(request,{'status':UNAUTHORIZED,
                                                'error':'Wrong user name and password'})

class TwitterAuth(ModelResource):

    class Meta:
        list_allowed_methods = ['post']

    def override_urls(self):
        return [url(r"^(?P<resource_name>%s)/signin%s$" %
            (self._meta.resource_name, trailing_slash()), 
            self.wrap_view('signin'), name="api_signin"), 
            ]

    def signin(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        
        postData = simplejson.loads(request.raw_post_data)
        twId = postData['id']
        token = postData['token']
        tokenSecret = postData['tokenSecret']
        
        #chek if user exists
        try:
            user = UserSocialAuth.objects.get(uid=twId,provider='twitter')
            key = getOrCreateKey(user.user)
            
            return self.create_response(request,{'status':OK,
                                                'token':key})
        except UserSocialAuth.DoesNotExist:
            #verify credentials against twitter API
            consumer = OAuthConsumer(TWITTER_CONSUMER_KEY,
                    TWITTER_CONSUMER_SECRET)
            uToken = Token(token, tokenSecret)
            client = OAuthClient(consumer,uToken)
            res, content = client.request(TWITTER_CHECK_AUTH, "GET")
            
            if res['status'] == '200':
                #credentials aproved
                contentJson = simplejson.loads(content)
                finalName = make_social_username(contentJson['screen_name'])
                newUser = User.objects.create_user(username=finalName,
                                                    email="")
                extraData = simplejson.dumps({u'access_token':u'oauth_token_secret=%s&oauth_token=%s',u'id': twId}) % (token, tokenSecret)

                newSocialU = UserSocialAuth.objects.create(user=newUser,
                                                provider='twitter',
                                                uid=twId,
                                                extra_data= extraData)
                newSocialU.save()
                key = getOrCreateKey(newUser)
                return self.create_response(request,{'status':OK,
                                                    'token':key})
            else:
                #credentials rejected
                return self.create_response(request,{'status': UNAUTHORIZED,
                                'error':'Twitter credentials denied'}) 

