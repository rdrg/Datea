# Django settings for datea project.

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from datea.local_settings import *
except ImportError:
    pass

import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_DEBUG = DEBUG
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
GRAPPELLI_ADMIN_TITLE = 'DATEA'

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Lima'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'site-static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'vqxc=2-+e&amp;og%)zt@%w84c2i)ahjg+frx%7khu5*kq=_273eq8'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'datea.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'datea.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, "templates"),
)

INSTALLED_APPS = (
    
    # standard 
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
    
    # extensions
    #'debug_toolbar',
    'registration',
    'social_auth',
    'south',
    'mptt',
    'tastypie',
    'bootstrap_toolkit',
    'django_extensions',
    #'easy_thumbnails',
    'sorl.thumbnail',
    'backbone_tastypie',
    
    # geodjango / location
    "django.contrib.gis",
    'olwidget',
    
    # datea
    'datea',
    'datea.datea_home',
    'datea.datea_image',
    'datea.datea_category',
    'datea.datea_channel',
    'datea.datea_profile',
    'datea.datea_action',
    'datea.datea_mapping',
    'datea.datea_vote',
    'datea.datea_follow',
    'datea.datea_api',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


AUTHENTICATION_BACKENDS = [
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    #"social_auth.backends.contrib.foursquare.FoursquareBackend",
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PROFILE_MODULE = 'datea_profile.DateaProfile'

LOGIN_URL = "/account/login/" 
#LOGIN_REDIRECT_URLNAME = "/" # CAMBIAR!
#LOGOUT_REDIRECT_URLNAME = "/"

LOGIN_REDIRECT_URL = '/' # CAMBIAR
LOGIN_ERROR_URL    = '/account/login'

# SOCIAL AUTH SETTINGS
from datea_profile.utils import make_social_username
SOCIAL_AUTH_USERNAME_FIXER = lambda u: make_social_username(u)
SOCIAL_AUTH_UUID_LENGTH = 16
SOCIAL_AUTH_EXPIRATION = 'expires'
SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True

ACCOUNT_ACTIVATION_DAYS = 7 

# EASY THUMBNAILS HAS PROBLEMS WITH TASTYPIE RELATED FIELDS OR DJANGO 1.4!!! 
#Thumbnails definitions
#THUMBNAIL_ALIASES = {
#    '': {
#        'image_thumb': {'size': (90,90)},
#        'profile_image': {'size': (50, 50), 'crop': True},
#        'profile_image_small': {'size': (25, 25), 'crop': True},
#        'profile_image_large': {'size': (130, 130), 'crop': True},
#        'category_image': {'size':(130,130), 'crop': True},
#        'marker_image': {'size':(0,38)},
#    },
#}
#THUMBNAIL_PRESERVE_EXTENSIONS = ('png',)

# OWN Implementation of presets for datea_image with sorl.thumbnails
THUMBNAIL_PRESETS = {
    'image_thumb': { "size": "90x90" },
    'image_thumb_medium': {"size": "160"},
    'image_thumb_large': {"size": "460x345"},
    'profile_image': {'size': "54x54", 'options': {'crop': 'center'}},
    'profile_image_small': {'size': "42x42", 'options': {'crop': 'center'}},
    'profile_image_large': {'size': "130x130", 'options': {'crop': 'center'}},
    'category_image': {'size': "130x130", 'options': {'crop': 'center'}},
    'marker_image': {'size':"x38", "options": {'format': 'PNG'}},
}
DEFAULT_PROFILE_IMAGE = os.path.join(MEDIA_ROOT, 'default/img/default-user.png')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
