from django.conf.urls import patterns, include, url
from tastypie.api import Api

from django.contrib import admin
admin.autodiscover()

#API resources
from datea_api.auth import Auth,TwitterAuth
v1_api = Api(api_name='v1')
v1_api.register(Auth())
v1_api.register(TwitterAuth())

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'datea.datea_home.views.home', name='home'),
    # url(r'^datea/', include('datea.foo.urls')),
    
    url(r'^api/',include(v1_api.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'', include('social_auth.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
)
