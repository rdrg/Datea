# -*- coding: utf-8 -*-
# Django settings for basic pinax project.

import os.path
import posixpath

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

DEFAULT_CHARSET = 'utf-8'

# django-compressor is turned off by default due to deployment overhead for
# most users. See <URL> for more information
COMPRESS = True
COMPRESS_ENABLED = True

INTERNAL_IPS = [
    "127.0.0.1",
]

ADMINS = [
    # ("Your Name", "your_email@domain.com"),
]

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.mysql", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": "datea3",                       # Or path to database file if using sqlite3.
        "USER": "root",                             # Not used with sqlite3.
        "PASSWORD": "huancaina",                         # Not used with sqlite3.
        "HOST": "",                             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",                             # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "America/Lima"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "es"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media", "static")

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = "/site_media/static/"

JQUERY_URL = 'js/jquery-1.7.min.js'

# OL DEV VERSION -> needed because problems with google layers
OL_API = os.path.join( STATIC_URL, "openlayers/OpenLayers.js")
#OL_API = 'http://openlayers.org/api/2.11/OpenLayers.js'
GOOGLE_API = "//maps.google.com/maps/api/js?v=3.2&sensor=false"

# Additional directories which hold static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
]

STATICFILES_FINDERS = [
    "staticfiles.finders.FileSystemFinder",
    "staticfiles.finders.AppDirectoriesFinder",
    "staticfiles.finders.LegacyAppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

DAJAXICE_MEDIA_PREFIX="dajaxice"

# Subdirectory of COMPRESS_ROOT to store the cached media files in
COMPRESS_OUTPUT_DIR = "cache"

# Make this unique, and don't share it with anybody.
SECRET_KEY = "99ig4m%kx2)$wfs3s36*l2w4)05hcrh$^99v^tkn_2^p)3zs)0"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.load_template_source",
    "django.template.loaders.app_directories.load_template_source",
    "django.template.loaders.eggs.load_template_source",
]

MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    #"django_openid.consumer.SessionConsumer",
    "django.contrib.messages.middleware.MessageMiddleware",
    "pinax.apps.account.middleware.LocaleMiddleware",
    "pagination.middleware.PaginationMiddleware",
    "pinax.middleware.security.HideSensistiveFieldsMiddleware",
    #"debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "datea3.urls"

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    
    "staticfiles.context_processors.static",
    
    "pinax.core.context_processors.pinax_settings",
    
    "social_auth.context_processors.social_auth_by_type_backends",
    
    "pinax.apps.account.context_processors.account",
    
    "notification.context_processors.notification",
    "announcements.context_processors.site_wide_announcements",
]

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.humanize",
    
    "pinax.templatetags",
    
    # theme
    "pinax_theme_bootstrap",
    
    # external pinax
    "notification", # must be first
    "staticfiles",
    "compressor",
    "debug_toolbar",
    "mailer",
    #"django_openid",
    "timezones",
    "emailconfirmation",
    "announcements",
    "pagination",
    #"idios",
    "metron",
    
    # external DATEA
    "south",
    "django_extensions",
    "mptt",
    #"categories",
    "sorl.thumbnail",
    #"easy_thumbnails",
    "oembed",
    "social_auth",
    "form_utils",
    "dajaxice",
    "dajax",
    "follow",
    "django.contrib.comments",
    "rulez",
    
    "feincms",
    "feincms.module.page",
    
    # GEODJANGO Y OLWIDGET
    "django.contrib.gis",
    "olwidget",
    
    # Pinax
    "pinax.apps.account",
    "pinax.apps.signup_codes",
    
    # DATEA
    "datea_images",
    "datea_profiles",
    "datea_report",
    "datea_vote",
    "datea_follow",
    "datea_comments",
    "datea_admin",
    "datea_content",
]

# EASY THUMBNAILS
THUMBNAIL_QUALITY = 90


COMPRESS_PRECOMPILERS = (
    ('text/less', '/usr/local/bin/lessc {infile} {outfile}'),
)
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter']

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

EMAIL_BACKEND = "mailer.backend.DbBackend"

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/profile/%s/" % o.username,
}

AUTH_PROFILE_MODULE = "datea_profiles.Profile"
NOTIFICATION_LANGUAGE_MODULE = "account.Account"

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = True

AUTHENTICATION_BACKENDS = [
    "social_auth.backends.twitter.TwitterBackend",
    "social_auth.backends.facebook.FacebookBackend",
    "social_auth.backends.google.GoogleOAuth2Backend",
    #"social_auth.backends.contrib.foursquare.FoursquareBackend",   
    "pinax.apps.account.auth_backends.AuthenticationBackend",
    'rulez.backends.ObjectPermissionBackend',
]

LOGIN_URL = "/account/login/" # @@@ any way this can be a url name?
LOGIN_REDIRECT_URLNAME = "home"
LOGOUT_REDIRECT_URLNAME = "home"

LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/account/login'

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

# SOCIAL AUTH SETTINGS
from apps.datea_profiles.utils import make_social_username
SOCIAL_AUTH_USERNAME_FIXER = lambda u: make_social_username(u)
SOCIAL_AUTH_UUID_LENGTH = 16
SOCIAL_AUTH_EXPIRATION = 'expires'
SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True

TWITTER_CONSUMER_KEY = 'RJqf4w0hdSusPFrLtfwkA'
TWITTER_CONSUMER_SECRET = 'drV2eP4zYgx8WqTSqzBAhxf6oeJcSMwTUVbBXpJ0qg'

FACEBOOK_APP_ID = '222271061161837'
FACEBOOK_API_SECRET = '37bf7dc201567ce71e673925d5891f4e'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']

GOOGLE_OAUTH2_CLIENT_ID = '324703561333.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = '8ipQymLrQL3lYnCGwqgxnP37'


DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# OLWIDGET OPTIONS
GOOGLE_API_KEY='AIzaSyCvq9gjYk6bnYMZ0rshPRYb5EhljTa2uzQ'

OLWIDGET_DEFAULT_OPTIONS = {
    'layers': ['google.streets', 'osm.mapnik']
}

#SERIALIZATION_MODULES = { 'geojson' : 'datea_report.geojson_serializer' }

FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'TINYMCE_JS_URL': os.path.join(STATIC_URL, 'tiny_mce/tiny_mce.js'),
    }



# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
