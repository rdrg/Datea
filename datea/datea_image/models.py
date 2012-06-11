from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField


class DateaImage(models.Model):
    
    image = ThumbnailerImageField(upload_to="images")
    user = models.ForeignKey(User, verbose_name=_("User"))
    order = models.IntegerField(blank=True, null=True, default=0)
    
    def __unicode__(self):
        return self.image.url
    
    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _('Images')
