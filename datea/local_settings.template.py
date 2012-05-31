DEBUG = True
TEMPLATE_DEBUG = DEBUG
MAINTENANCE_MODE = False


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # POSTGIS!! -> see geodjango
        'NAME': 'your_postgis_db',          #
        'USER': 'xxx',                      # Not used with sqlite3.
        'PASSWORD': 'xxx',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

#mail server settings
EMAIL_HOST = ''
EMAIL_HOST_USER= ''
DEFAULT_FROM_EMAIL = ''
EMAIL_HOST_PASSWORD= ''
EMAIL_PORT= '587'
EMAIL_USE_TLS = True
SEND_BROKEN_LINK_EMAILS = True
EMAIL_SUBJECT_PREFIX = '[Datea]'
