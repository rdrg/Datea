from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("datea.datea_profile.views",
    url("^edit_profile/notify_settings/", 'redirect_notify_settings'),
    url("^profile/(?P<id>[0-9]+)/", 'redirect_user'),
    url("^perfil/(?P<id>[0-9]+)/", 'redirect_user'),
)