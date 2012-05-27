from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from datea.datea_image.models import DateaImage
from django.utils.translation import ugettext_lazy as _


class DateaSubpage(models.Model):
    
    user = models.ForeignKey(User, verbose_name=_('User'), related_name="subpages")
    
    name = models.CharField( _("Name"), max_length=100)
    slug = models.SlugField( _("Slug"), max_length=30, help_text=_("A string of text as a short id for use at the url of this map (alphanumeric and dashes only"))
    published = models.BooleanField( _("Published"), default=True)
    
    # timestamps
    created = models.DateTimeField( _('created'), auto_now_add=True)
    modified = models.DateTimeField( _('modified'), auto_now=True)
    
    # text input fields
    short_description = models.CharField( _("Short description / Slogan"), blank=True, null=True, max_length=140, help_text=_("A short description or slogan (max. 140 characters)."))
    mission = models.TextField( _("Mission / Objectives"), blank=True, null=True, max_length=500, help_text=_("max. 500 characters"))
    information_destiny = models.TextField( _("What happens with the data?"), max_length=500, help_text=_("Who receives the information and what happens with it? (max 500 characters)"))
    long_description = models.TextField( _("Description"), blank=True, null=True, help_text=_("Long description (optional)"))
    report_success_message = models.TextField( _("Report success message"), blank=True, null=True, max_length=140, help_text=_("The message someone sees when succesfully filing a report (max. 140 characters)"))
    
    # images
    image = models.ForeignKey( DateaImage, verbose_name=_("Site image"), blank=True, null=True, related_name="subpage_image")
    logo = models.ForeignKey( DateaImage, verbose_name=_("Logo"), blank=True, null=True, related_name="subpage_logo")
    
    # site object for the subdomain
    site = models.OneToOneField( Site, verbose_name=_("Site"))
    
    def __unicode__(self):
        return self.name+' ['+self.site.domain+']'
    
    class Meta:
        verbose_name = _('Sub-page')
        verbose_name_plural = _('Sub-pages')
    
    

