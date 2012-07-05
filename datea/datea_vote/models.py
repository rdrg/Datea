from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class DateaVote(models.Model):
    
    user = models.ForeignKey(User, related_name="votes")
    created = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(default=1)
    
    # generic content type relation to voted object
    # content_type = models.ForeignKey(ContentType)
    # object_id = models.PositiveIntegerField()
    # content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    object_type = models.CharField(max_length=255)
    object_id = models.PositiveIntegerField()
    
    def __unicode__(self):
        return "Datea vote"
    

