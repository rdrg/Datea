from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns("datea_report.views",
    
    #++++++++++++++
    # REPORT CREATE
    #url(r"^create/$", 'report_create', name="datea_report_create_default"),
    #url(r"^(?P<env_slug>[a-z0-9-]+)/create", 'report_create', name="datea_report_create"),
    #+++++++++++++++
    # REPORT UPDATE
    # 1. update en interfase
    #url(r"^update/(?P<report_id>\d+)/$", 'report_update', name="datea_report_update_default"),
    #url(r"^update/(?P<env_slug>[a-z0-9-]+)/(?P<report_id>\d+)/$", 'report_update', name="datea_report_update"), 
    
    # ENVIRONMENT
    #url(r"^(?P<env_slug>[a-z0-9-]+)/$", 'home', name="environment_home"),
    #url(r"^(?P<env_slug>[a-z0-9-]+)/(?P<cat_slug>[a-z0-9-]+)/$", 'main_category', name='main_category_default'),
    #url(r"^(?P<env_slug>[a-z0-9-]+)/(?P<cat_slug>[a-z0-9-]+)/(?P<tab>[a-z0-9-/]+)/$", 'main_category', name='main_category_tab'),
    
    url(r"^(?P<env_slug>[a-z0-9-]+)/$", 'environment_tab', name='environment_home'),
    url(r"^(?P<env_slug>[a-z0-9-]+)/(?P<hash_path>[a-z0-9-/]+)", 'environment_tab', name="environment_tab"),
    
    #++++++++++++++++++++++++
    # REPORT VIEWS
    url(r"^(?P<env_slug>[a-z0-9-]+)/reports/(?P<cat_slug>[a-z0-9-]+)/$", 'environment_tab', name="reports_list"), 
    url(r"^(?P<env_slug>[a-z0-9-]+)/reports/(?P<cat_slug>[a-z0-9-]+)/(?P<report_id>\d+)/$", 'environment_tab', name="report_detail"),
    url(r"^(?P<env_slug>[a-z0-9-]+)/new-report/(?P<cat_slug>[a-z0-9-]+)/$", 'environment_tab', name="new_report"),      
    
    # PIE CLUSTER
    url(r"^piecluster$", 'get_pie_cluster'),
    url("^svgcircle", 'get_circle')

)

