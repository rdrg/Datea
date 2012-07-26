from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("datea.datea_mapping.views",
    
    #url("^mapping/(?P<path>[a-z0-9-/]+)", 'redirect_to_hash'),
    url("^mapping/(?P<mapping_id>[a-z0-9]+)/reports/item(?P<map_item_id>[0-9]+)/", 'get_map_item', name='map_item'),
    url("^mapping/(?P<mapping_id>[a-z0-9]+)/", 'get_mapping', name='mapping'),
    
    # PIE CLUSTERS FRO OPENLAYERS
    # png graphic generation for map clusters (requires imagemagick convert)
    url(r"^png/piecluster$", 'get_pie_cluster'),
    url("^png/svgcircle", 'get_circle'),
)