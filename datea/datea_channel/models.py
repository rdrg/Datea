from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class DateaChannel(models.Model):
    
    user = models.ForeignKey(User, verbose_name=_('User'), related_name="channels")
    
    published = models.BooleanField( _("Published"), default=False)
    
    short_description = models.CharField( _("Short description / Slogan"), blank=True, null=True, max_length=140, help_text=_("A short description or slogan (max. 140 characters)."))
    mission = models.TextField( _("Mission / Objectives"), blank=True, null=True, max_length=500, help_text=_("max. 500 characters"))
    information_destiny = models.TextField( _("What happens with the data?"), max_length=500, help_text=_("Who receives the information and what happens with it? (max 500 characters)"))
    long_description = models.TextField( _("Description"), blank=True, null=True, help_text=_("Long description (optional)"))
    
    # site object for the subdomain
    site = models.OneToOneField( Site, verbose_name=_("Site"))
    
    def __unicode__(self):
        return self.user.username+"'s channel"
    
    class Meta:
        verbose_name = _('Channel')
        verbose_name_plural = _('Channels')