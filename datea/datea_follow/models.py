from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Create your models here.

class DateaFollow(models.Model):
    
    user = models.ForeignKey(User, related_name="follows")
    created = models.DateTimeField(_('created'), auto_now_add=True)
    
    # generic content type relation to followed object
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    followed_object = generic.GenericForeignKey()
    
    class Meta:
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')
        
