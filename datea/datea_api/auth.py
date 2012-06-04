from django.conf.urls.defaults import url 
from django.contrib.auth.models import User
from django.utils import simplejson
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm

from tastypie.resources import ModelResource 
from tastypie.utils import trailing_slash 

from oauth2 import Client as OAuthClient, Consumer as OAuthConsumer, Token
from datea.settings import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
from social_auth.backends.twitter import TWITTER_CHECK_AUTH
from social_auth.models import UserSocialAuth

from registration.backends import get_backend

from utils import getOrCreateKey, getUserByKey
from status_codes import *
from datea.datea_profile.utils import make_social_username

END_POINT_NAME = 'accounts'

class Accounts(ModelResource):
    class Meta:
        allowed_methods = ['post']

    def override_urls(self):
        return [
            #create account
            url(r"^(?P<resource_name>%s)/create%s$" %
            (END_POINT_NAME, trailing_slash()), 
            self.wrap_view('create'), name="api_create_account"), 
            
            #signin
            url(r"^(?P<resource_name>%s)/signin%s$" %
            (END_POINT_NAME, trailing_slash()),
            self.wrap_view('signin'), name="api_signin"),

            #password reset
            url(r"^(?P<resource_name>%s)/passwordReset%s$" %
            (END_POINT_NAME, trailing_slash()),
            self.wrap_view('passwordReset'), name="api_password_reset"),
            
            #twitter
            url(r"^(?P<resource_name>%s)/twitter%s$" %
            (END_POINT_NAME, trailing_slash()),
            self.wrap_view('twitter'), name="api_twitter_account"),
            ]

    def create(self, request, **kwargs):
        print "@ create account"
        self.method_check(request, allowed=['post'])
        
        backend = get_backend('registration.backends.default.DefaultBackend')
        postData = simplejson.loads(request.raw_post_data)

        args = {'username':postData['username'],
                'email' : postData['email'],
                'password1' : postData['password']}
        print "post data"
        print args
        print "trying to create account"
        newUser = backend.register(request,**args)
        
        print "user created"
        if newUser:
            return self.create_response(request,{'status': OK,
                'message': 'Please check your email !!'})

        else:
            return self.create_response(request,{'status': SYSTEM_ERROR,
                                    'error': 'Something is wrong >:/ '})
        

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

    def passwordReset(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        postData = simplejson.loads(request.raw_post_data)
        key = postData['token']

        user = getUserByKey(key)

        if user is not None:
            if user.is_active:
                data = {'email': user.email}
                resetForm = PasswordResetForm(data)
            
                if resetForm.is_valid():
                    resetForm.save()
            
                    return self.create_response(request,{'status':OK,
                        'message': 'check your email for instructions'})
                else:
                    return self.create_response(request, 
                            {'status': SYSTEM_ERROR,
                            'message': 'form not valid'})
            else:
                return self.create_response(request, {'status':FORBIDDEN,
                    'message':'Account disabled'})
        else:
            return self.create_response(request, {'status': UNAUTHORIZED,
                        'error': 'User does not exists'})


    def twitter(self, request, **kwargs):
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

