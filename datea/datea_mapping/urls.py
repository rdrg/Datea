from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("datea.datea_mapping.views",
    
    url("^mapping/(?P<path>[a-z0-9-/]+)", 'redirect_to_hash'),
    
    # PIE CLUSTERS FRO OPENLAYERS
    # png graphic generation for map clusters (requires imagemagick convert)
    url(r"^png/piecluster$", 'get_pie_cluster'),
    url("^png/svgcircle", 'get_circle'),
)