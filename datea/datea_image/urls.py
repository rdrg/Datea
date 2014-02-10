from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("datea.datea_image.views",
    url(r"^delete/(?P<pk>\d+)/$", 'delete_image'),
    url(r"^save/$", 'save_image'),
    url(r"^api_save/$", 'save_image_api'),
    url(r"^mobile_save/$",'mobile_image_save'),
    #url(r("^get/(?P<pk>\d+)/(?P<size>\d+)/"), "get_image"),
)
