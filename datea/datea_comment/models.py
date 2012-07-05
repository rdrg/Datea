from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
# Create your models here.

class DateaComment(models.Model):
    
    user = models.ForeignKey(User, verbose_name=_('User'), related_name='comments')
    created = models.DateTimeField(_('created'), auto_now_add=True)
    comment = models.TextField(_('Comment'))
    reply_to = models.ForeignKey('self', null=True, blank=True, related_name="replies")
    
    # generic content type relation to commented object
    # content_type = models.ForeignKey(ContentType)
    # object_id = models.PositiveIntegerField()
    # content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    # do we need content type relation? perhaps this is more simple and fast...
    object_type = models.CharField(_('Object Name'), max_length=50) # object typeid -> whatever
    object_id = models.PositiveIntegerField(_('Object id')) # object id
    
    def save(self, *args, **kwargs):
        
        ctype = ContentType.objects.get(model=self.object_type.lower())
        receiver_object = ctype.get_object_for_this_type(pk=self.object_id)
        
        
        super(DateaComment, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "Datea vote"
    
    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
    
