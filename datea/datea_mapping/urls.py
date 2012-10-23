from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("datea.datea_mapping.views",
    
    #url("^mapping/(?P<path>[a-z0-9-/]+)", 'redirect_to_hash'),
    # EN
    url("^mapping/(?P<mapping_id>[a-z0-9]+)/reports/item(?P<map_item_id>[0-9]+)/", 'get_map_item', name='map_item'),
    url("^mapping/(?P<mapping_id>[a-z0-9]+)/", 'get_mapping', name='mapping'),
    # ES
    url("^mapeo/(?P<mapping_id>[a-z0-9]+)/dateos/(?P<map_item_id>[0-9]+)/", 'get_map_item', name='map_item'),
    url("^mapeo/(?P<mapping_id>[a-z0-9]+)/", 'get_mapping', name='mapping'),
    
    # PIE CLUSTERS FRO OPENLAYERS
    # png graphic generation for map clusters (requires imagemagick convert)
    url(r"^png/piecluster$", 'get_pie_cluster'),
    url("^png/svgcircle", 'get_circle'),
    
    # CSV EXPORT
    url(r"csv_export/mapping/(?P<mapping_id>[0-9]+)/$", 'csv_export', name='csv_export')
)