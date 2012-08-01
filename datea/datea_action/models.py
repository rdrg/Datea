from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from datea.datea_category.models import DateaCategory
from mptt.fields import TreeForeignKey
from django.contrib.contenttypes.models import ContentType
from datea.datea_image.models import DateaImage
# Create your models here.


class SubclassingQuerySet(models.query.GeoQuerySet):
    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model) :
            return result.as_leaf_class()
        else :
            return result
    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.as_leaf_class()


class DateaActionManager(models.GeoManager):
    def get_query_set(self):
        return SubclassingQuerySet(self.model)


class DateaAction(models.Model):
    
    user = models.ForeignKey(User, verbose_name=_('User'), related_name="actions")
    
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=30, help_text=_("A string of text as a short id for use at the url of this map (alphanumeric and dashes only"))
    published = models.BooleanField(_("Published"), default=True)
    
    # timestamps
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    
    short_description = models.CharField(_("Short description / Slogan"), blank=True, null=True, max_length=140, help_text=_("A short description or slogan (max. 140 characters)."))
    hashtag = models.CharField(_("Hashtag"), blank=True, null=True, max_length=100, help_text=_("A twitter hashtag for your action"))
    category = TreeForeignKey(DateaCategory, verbose_name=_("Category"), null=True, blank=True, default=None, related_name="actions", help_text=_("Choose a category for this action")) 
    featured = models.BooleanField(_('Featured'), default=False)
    
    image = models.ForeignKey(DateaImage, verbose_name=_('Image'), blank=True, null=True, related_name="actions")
    
    action_type = models.CharField(_('Action type'), max_length=100, blank=True, null=True)
    
    # statistics
    item_count = models.PositiveIntegerField(_("Item count"), default=0)
    user_count = models.PositiveIntegerField(_("Participant count"), default=0)
    comment_count = models.PositiveIntegerField(_('Comment count'), default=0)
    follow_count = models.PositiveIntegerField(_('Follower count'), default=0)
    
    # generic relation to subclasses
    content_type = models.ForeignKey(ContentType,editable=False,null=True)
    objects = DateaActionManager()
    
    def get_absolute_url(self):
        return '/'+self.action_type+'/'+str(self.pk)
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        print "SAVE"
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
            super(DateaAction, self).save(*args, **kwargs)
            
    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if (model == DateaAction):
            return self
        return model.objects.get(id=self.id)
    
    
    



