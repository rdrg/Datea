from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("datea.datea_profile.views",
    url("^edit_profile/notify_settings/", 'redirect_notify_settings'),
    url("^user/(?P<id>[0-9]+)/", 'redirect_user'),
)