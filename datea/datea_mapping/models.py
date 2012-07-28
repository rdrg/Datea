from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags

from datea.datea_image.models import DateaImage 
from datea.datea_action.models import DateaAction
from datea.datea_category.models import DateaCategory, DateaFreeCategory
from mptt.fields import TreeForeignKey, TreeManyToManyField
from django.db.models.signals import post_save, m2m_changed
from signals import map_item_response_created

        
class DateaMapping(DateaAction):
    
    label = _('mapping')
    
    # text input fields
    mission = models.TextField(_("Mission / Objectives"), 
                            blank=True, 
                            null=True, 
                            max_length=500, 
                            help_text=_("max. 500 characters"))
    
    information_destiny = models.TextField(_("What happens with the data?"), 
                            max_length=500, 
                            help_text=_("Who receives the information and what happens with it? (max 500 characters)")
                        )
    
    long_description = models.TextField(_("Description"), 
                            blank=True, 
                            null=True, 
                            help_text=_("Long description (optional)"))
    
    report_success_message = models.TextField(_("Item submitted success message"), 
                            blank=True, 
                            null=True, 
                            max_length=140, 
                            help_text=_("The message someone sees when succesfully filing a report (max. 140 characters)"))
    
    image = models.ForeignKey(DateaImage, verbose_name=_('Image'), blank=True, null=True, related_name="mappings")
   
    default_color = models.CharField(_('Default Item Color'), max_length=7, blank=True, default="#ff9c00", help_text=_("Default color for map items (used when there's no categories defined)."))
    # ZONES
    #zones = models.ManyToManyField(Zone, blank=True, null=True, default=None)
    
    # CATEGORIES / VARIABLES
    item_categories = TreeManyToManyField(DateaFreeCategory, 
                            verbose_name=_("Map item Categories"), 
                            blank=True, null=True, 
                            default=None, 
                            help_text=_("Categories for Mapped Items"), 
                            related_name="mappings")
    
    # GEO:
    center = models.PointField(_("Center"), blank=True, null=True, spatial_index=False)
    boundary = models.PolygonField(_("Boundary"), blank=True, null=True, spatial_index=False)
    
    # Object Manager from geodjango
    objects = models.GeoManager()
        
    class Meta:
        verbose_name = _("Mapping")
        verbose_name_plural = _("Mappings")
    
    def save(self, *args, **kwargs):
        
        self.action_type = 'mapping'
        
        if self.center == None and self.boundary != None:
            self.center = self.boundary.centroid
            self.center.srid = self.boundary.get_srid()
        
        self.save_base()
        super(DateaMapping, self).save(*args, **kwargs)
    


class DateaMapItem(models.Model):
    
    label = _('map_item')
    
    user = models.ForeignKey(User, verbose_name=_('User'), related_name="map_items")
    
    # timestamps
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    
    # status, published
    published = models.BooleanField(_("published"), default=True)
    status_choices = (
            ('new',_('new')), 
            ('reviewed', _('reviewed')), 
            ('solved', _('solved'))
        )
    status = models.CharField(_("status"), max_length=15, choices=status_choices, default="new")
    
    # content
    content = models.TextField(_("Content"))
    images = models.ManyToManyField(DateaImage, verbose_name=_('Images'), null=True, blank=True, related_name="map_item_images")
    
    # location
    position = models.PointField(_('Position'), blank=True, null=True, spatial_index=False)
    address = models.CharField(_('Address'), max_length=255, blank=True, null=True)
    
    # relation to mapping object: UPDATE -> refer to mapping as an action. More generic!!
    #mapping = models.ForeignKey('DateaMapping', related_name="map_items_old")
    action = models.ForeignKey('DateaMapping', related_name="map_items")
    
    # category
    category = TreeForeignKey(DateaFreeCategory, verbose_name=_("Category"), null=True, blank=True, default=None, related_name="map_items")
    
    # stats
    vote_count = models.IntegerField(default=0, blank=True, null=True)
    comment_count = models.IntegerField(default=0,blank=True, null=True)
    follow_count = models.IntegerField(default=0, blank=True, null=True)
    reply_count = models.IntegerField(default=0, blank=True, null=True)
    
    # Object Manager from geodjango
    objects = models.GeoManager()
    
    def save(self, *args, **kwargs):
        super(DateaMapItem, self).save(*args, **kwargs)
        self.action.item_count = self.action.map_items.filter(published=True).count()
        users = []
        for item in self.action.map_items.all():
            if item.user.is_active and item.user.pk not in users:
                users.append(item.user.pk)
        self.action.user_count = len(users)
        self.action.save()
    
    def get_absolute_url(self):
        return self.action.get_absolute_url()+'/reports/item'+str(self.pk)  
    
    def __unicode__(self):
        return self.user.username+': '+strip_tags(self.content)[:100]
    
    class Meta:
        verbose_name = _('Map Item')
        verbose_name_plural = _('Map Items')
        


class DateaMapItemResponse(models.Model):
    
    user = models.ForeignKey(User, verbose_name=_("User"), related_name="map_item_responses")
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    map_items = models.ManyToManyField('DateaMapItem', verbose_name=_("Map Items"), related_name="responses") 
    content = models.TextField(_("Response"))
    
    # call this after model and m2m fields have been saved    
    def update_item_stats(self):
        for item in self.map_items.all():
            item.reply_count = item.responses.count()
            item.save()
        
    def __unicode__(self):
        return strip_tags(self.content)[:80]
    
    class Meta:
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')


def on_response_save(sender, instance, **kwargs):
    instance.update_item_stats()
map_item_response_created.connect(on_response_save, sender=DateaMapItemResponse)

        
    

    

    
    
    
