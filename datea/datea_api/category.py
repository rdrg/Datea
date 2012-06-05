from tastypie import fields
from tastypie.resources import ModelResource
from datea.datea_category.models import DateaCategory, DateaFreeCategory

class CategoryResource(ModelResource):
    class Meta:
        queryset = DateaCategory.objects.all()
        resource_name = 'category'
  
        
class FreeCategoryResource(ModelResource):
    mappings = fields.ToOneField('datea.datea_api.mapping.MappingResource', 'mapping', full=True, null=True)
    
    class Meta:
        queryset = DateaFreeCategory.objects.all()
        resource_name = 'free_category'
        allowed_methods = ['get']