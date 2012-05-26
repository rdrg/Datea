from django.conf.urls.defaults import patterns, url


urlpatterns = patterns("datea_images.views",
    url(r"^delete/(?P<pk>\d+)/$", 'delete_image'),
    url(r"^save/$", 'save_image'),
    url(r"show/(?P<size>[a-z0-9]+)/(?P<pk>\d+)/$", "show_image", name="datea_image_show")     
)