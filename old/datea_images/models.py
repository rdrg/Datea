from django.db import models

from sorl.thumbnail import ImageField
from sorl.thumbnail import get_thumbnail
from django.contrib.auth.models import User

# Create your models here.

class DateaImage(models.Model):
    
    image = ImageField(upload_to="images")
    author = models.ForeignKey(User, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True, default=0)
    is_avatar = models.BooleanField(default=False)
    
    def get_thumbnail(self, **kwargs):
        return get_thumbnail(self.image.file, **kwargs)
    
    def __unicode__(self):
        return "imagen"
    
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^datea_images\.fields\.DateaImageM2MField"])