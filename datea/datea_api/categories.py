from tastypie.resources import ModelResource
from datea.datea_category.models import DateaCategory, DateaFreeCategory

class DateaCategoryResource(ModelResource):
    class Meta:
        queryset = DateaCategory.objects.all()
        resource_name = 'datea_category'
  
        
class DateaFreeCategoryResource(ModelResource):
    class Meta:
        queryset = DateaFreeCategory.objects.all()
        resource_name = 'datea_free_category'