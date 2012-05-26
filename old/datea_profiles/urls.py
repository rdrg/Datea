from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("datea_profiles.views",
   
   # my profile detail default
   url('^profiles/my-profile$', 'view_profile', name="view_profile_own_default"),
   
   # a profile detail default
   url('^profiles/detail/(?P<username>[a-z0-9-_]+)$', 'view_profile', name="view_profile_default"),
   
   # my profile detail inside environment
   url('^report/(?P<env_slug>[a-z0-9-]+)/my-profile/$', 'view_profile', name="view_profile_own_env"),
   # a profile inside environment
   url('^report/(?P<env_slug>[a-z0-9-]+)/people/detail/(?P<username>[a-z0-9-_]+)$', 'view_profile', name="view_profile_env"),
   
   # default edit account, edit profile 
   url(r"^profiles/edit_account/$", 'edit_account', name="edit_account_default"),
   url(r"^profiles/edit_profile/$", 'edit_account', name="edit_profile_default"),
   url(r"^profiles/edit_follow/$", 'edit_account', name="edit_follow_default"),
   # environment edit account, edit profile
   url('^report/(?P<env_slug>[a-z0-9-]+)/my-profile/edit-account$', 'edit_account', name="edit_account_env"),
   url('^report/(?P<env_slug>[a-z0-9-]+)/my-profile/edit-profile$', 'edit_account', name="edit_profile_env"),
   url('^report/(?P<env_slug>[a-z0-9-]+)/my-profile/edit-notification$', 'edit_account', name="edit_notification_env"),
   
   url(r"^profiles/upload_avatar/$", 'upload_avatar', name="upload_avatar"),                                 
)

