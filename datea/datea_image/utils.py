from django.conf import settings
from sorl.thumbnail import get_thumbnail


def get_image_thumb(url, thumb_preset = 'image_thumb'):

    Preset = settings.THUMBNAIL_PRESETS[thumb_preset]
    #preserve format
    ext = url.split('.')[-1].upper()
    if ext not in ['PNG', 'JPG']:
        ext = 'JPG'
    options = {'format': ext }
    if 'options' in Preset:
        options.update(Preset['options'])
    return get_thumbnail(url, Preset['size'], options=options)