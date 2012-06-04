from tastyPie import fields
from tastypie.resources import ModelResource
from datea.datea_mapping.models import DateaMapping, DateaMapItem

class DateaMappingResource(ModelResource):
    fields.toManyField('datea.datea_api.category.DateaFreeCategoryResource', 'item_categories_set', related_name='mappings')
    
    class Meta:
        queryset = DateaMapping.objects.all()
        resource_name = 'datea_mapping'
        
class DateaMapItemResource(ModelResource):
    class Meta:
        queryset = DateaMapping.objects.all()
        resource_name = 'datea_map_item'