from django.db import models

# Mptt: trees of hierarchically arranged models
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.contrib.auth.models import User

from datea.datea_image.models import DateaImage 

from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _


class DateaCategoryBase(MPTTModel):
    
    user = models.ForeignKey(User)
    
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=50, blank=True, null=True)
    description = models.TextField(_('Description'), max_length=500, blank=True, null=True)
    active = models.BooleanField(_('is active'), default=True)
    color = models.CharField( max_length=7, default='#cccccc')
    
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if self.slug == 'slug' or self.slug == None or self.slug == '':
            self.slug = slugify(self.name)
        super(DateaCategoryBase, self).save(*args, **kwargs)


# FIX Categories
class DateaCategory(DateaCategoryBase):
    
    image = models.ForeignKey( DateaImage, verbose_name=_('Image'), blank=True, null=True, related_name="categories_image")
    marker_image = models.ForeignKey( DateaImage, verbose_name=_('Marker image'), blank=True, null=True,related_name="categories_marker")    
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')       

# Categories added by normal users
class DateaFreeCategory(DateaCategoryBase):
    
    image = models.ForeignKey( DateaImage, verbose_name=_('Image'), blank=True, null=True, related_name="free_categories_image")
    marker_image = models.ForeignKey( DateaImage, verbose_name=_('Marker image'), blank=True, null=True,related_name="free_categories_marker")    
    
    class Meta:
        verbose_name = _('Free category')
        verbose_name_plural = _('Free categories')

