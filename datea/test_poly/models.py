#from django.db import models
from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet

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

class MealManager(models.GeoManager):
    def get_query_set(self):
        return SubclassingQuerySet(self.model)

class Meal (models.Model) :
    
    name = models.TextField(max_length=100)
    content_type = models.ForeignKey(ContentType,editable=False,null=True)
    objects = MealManager()
    
    def save(self, *args, **kwargs):
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
            super(Meal, self).save(*args, **kwargs)

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if (model == Meal):
            return self
        return model.objects.get(id=self.id)

    def __unicode__(self):
        return self.name
    
class Salad (Meal) :
    too_leafy = models.BooleanField(default=False)
    objects = MealManager()
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.save_base()
        super(Salad, self).save(*args, **kwargs)
    
class Desert (Meal):
    foor = models.CharField(max_length="200")
    objects = MealManager()
    
    def save(self, *args, **kwargs):
        self.save_base()
        super(Salad, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name

