from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
#from easy_thumbnails.fields import ThumbnailerImageField
#from easy_thumbnails.files import get_thumbnailer
from sorl.thumbnail import default, ImageField, get_thumbnail
from django.conf import settings
from django.db.models.deletion import Collector
from django.db import router


class DateaImage(models.Model):

    image = ImageField(upload_to="images")  
    user = models.ForeignKey(User, verbose_name=_("User"))
    order = models.IntegerField(blank=True, null=True, default=0)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    
    
    def __unicode__(self):
        return self.image.url
    
    
    def get_thumb(self, preset='image_thumb'):
        Preset = settings.THUMBNAIL_PRESETS[preset]
        #preserve format
        ext = self.image.url.split('.')[-1].upper()
        if ext not in ['PNG', 'JPG'] or ext == 'JPG':
            ext = 'JPEG'
        options = {'format': ext }
        if 'options' in Preset:
            options.update(Preset['options'])
        return get_thumbnail(self.image, Preset['size'], **options).url
    
    
    def save(self, *args, **kwargs):

        if not self.image._file:
            image = default.engine.get_image(self.image)
            (self.width, self.height) = default.engine.get_image_size(image)
        super(DateaImage, self).save(*args, **kwargs)
        
    def delete(self, using=None):
        self.clear_nullable_related()
        super(DateaImage, self).delete(using=using)
        
    def clear_nullable_related(self):
        """
        Recursively clears any nullable foreign key fields on related objects.
        Django is hard-wired for cascading deletes, which is very dangerous for
        us. This simulates ON DELETE SET NULL behavior manually.
        """
        for related in self._meta.get_all_related_objects():
            accessor = related.get_accessor_name()
            related_set = getattr(self, accessor)

            if related.field.null:
                related_set.clear()
                print vars(related_set.all())
            else:
                for related_object in related_set.all():
                    related_object.clear_nullable_related()

        
    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _('Images')
