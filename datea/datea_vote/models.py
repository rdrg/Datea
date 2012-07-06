from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _


class DateaVote(models.Model):
    
    label = _('vote')
    
    user = models.ForeignKey(User, related_name="votes")
    created = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(default=1)
    
    # generic content type relation to voted object
    # content_type = models.ForeignKey(ContentType)
    # object_id = models.PositiveIntegerField()
    # content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    object_type = models.CharField(max_length=255)
    object_id = models.PositiveIntegerField()
    
    
    def save(self, *args, **kwargs):
        # update comment stats on voted object  
        if self.pk == None:
            ctype = ContentType.objects.get(model=self.object_type.lower())
            receiver_obj = ctype.get_object_for_this_type(pk=self.object_id)
            if hasattr(receiver_obj, 'vote_count'):
                receiver_obj.vote_count += 1
                receiver_obj.save()
        super(DateaVote, self).save(*args, **kwargs)
        
        
    def delete(self, using=None):
        # update comment stats on voted object 
        ctype = ContentType.objects.get(model=self.object_type.lower())
        receiver_obj = ctype.get_object_for_this_type(pk=self.object_id)
        if hasattr(receiver_obj, 'vote_count'):
            receiver_obj.vote_count -= 1
            receiver_obj.save()
        super(DateaVote, self).delete(using=using)
    
    def __unicode__(self):
        return "Datea vote"
    

