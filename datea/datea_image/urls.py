from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("datea.datea_image.views",
    url(r"^delete/(?P<pk>\d+)/$", 'delete_image'),
    url(r"^save/$", 'save_image'),
)