from django.conf.urls.defaults import patterns, url 
from django.contrib.auth.models import User
from django.utils import simplejson

from django.contrib.auth import authenticate, login 
from tastypie.resources import ModelResource 
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.utils import trailing_slash 

class Dauth(ModelResource):
    class Meta:
        queryset = User.objects.all()
        list_allowed_methods = ['post']

    def override_urls(self):
        return [url(r"^(?P<resource_name>%s)/signin%s$" %
            (self._meta.resource_name, trailing_slash()), 
            self.wrap_view('signin'), name="api_signin"), 
            ]

    def signin(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        
        post_data = simplejson.loads(request.raw_post_data)
        username = post_data['username']
        password = post_data['password']

        user = authenticate(username= username,
                            password= password)

        if user is not None:
            if user.is_active:
                login(request,user)
                return self.create_response(request,{'success':True})
            else:
                return self.create_response(request,{'success':False,
                                                    'error': 'Account disabled'})
        else:
            return self.create_response(request,{'success':False,
                                                'error':'Wrong user name and password'})
        
