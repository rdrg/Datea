from tastypie import fields
from tastypie.resources import ModelResource
from datea.datea_mapping.models import DateaMapping, DateaMapItem
from datea.datea_api.category import FreeCategoryResource

class MappingResource(ModelResource):
    item_categories = fields.ToManyField('datea.datea_api.category.FreeCategoryResource', 'datea_free_category', full=True, null=True)
    
    class Meta:
        queryset = DateaMapping.objects.all()
        resource_name = 'datea_mapping'
        
class MapItemResource(ModelResource):
    class Meta:
        queryset = DateaMapping.objects.all()
        resource_name = 'datea_map_item'