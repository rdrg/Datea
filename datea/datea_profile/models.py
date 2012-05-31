from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from datea.datea_image.models import DateaImage 

class DateaProfile(models.Model):
    
    user = models.ForeignKey(User, verbose_name=_("User"))
    created = models.DateTimeField( _('created'), auto_now_add=True)
    
    first_name = models.CharField(_("First name"), max_length=50, null=True, blank=True)
    last_name = models.CharField(_("Last name"), max_length=50, null=True, blank=True)
    
    image = models.ForeignKey(DateaImage, blank=True, null=True, related_name="profile_image")
    image_social = models.ForeignKey(DateaImage, blank=True, null=True, related_name="profile_image_social")
    
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        
    def __unicode__(self):
        name = ''
        if self.fisrt_name != '' or self.last_name:
            name = self.fisrt_name + ' ' + self.last_name + ' '
        return name + ' ('+self.user.username+')'
    
    


