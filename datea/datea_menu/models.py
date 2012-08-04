from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.contrib.flatpages.models import FlatPage

class Item(models.Model) :
    name = models.CharField(max_length=50 )
    alt = models.CharField(max_length=150 )
    url = models.CharField(max_length=100 )
    order = models.IntegerField(blank = True, null=True)
    visible = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        model = self.__class__
        if self.order is None:
            try:
                last = model.objects.order_by('-order')[0]
                print '--------', last.order
                self.order = last.order + 1
            except IndexError:
                self.order = 0

        return  super(Item, self).save(*args,**kwargs)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.name
    


class DateaMenuItem(MPTTModel):
    name = models.CharField(_('Menu title'), max_length=50)
    page_title = models.CharField(_('Page title'), max_length=150, null=True, blank=True)
    visible = models.BooleanField(_('Visible'), default=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')  
    page = models.ForeignKey(FlatPage, verbose_name=_('Page'), blank=True, null=True)
    menu_root_id = models.SlugField(_('Menu root id'), null=True, blank=True, help_text=_("String to identify this menu to the datea_menu template tags"))
    external_url = models.URLField(_('External url'), verify_exists=False, null=True, blank=True)
    
    def __unicode__(self):
        return self.name 
    
    