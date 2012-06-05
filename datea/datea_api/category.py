from tastypie import fields
from tastypie.resources import ModelResource,ALL
from datea.datea_category.models import DateaCategory, DateaFreeCategory

class CategoryResource(ModelResource):
    class Meta:
        queryset = DateaCategory.objects.all()
        resource_name = 'category'
  
        
class FreeCategoryResource(ModelResource):
    image = fields.ToOneField('datea.datea_api.image.ImageResource',
            attribute='image', full=True, null=True)
    marker_image = fields.ToOneField('datea.datea_api.image.ImageResource',
            attribute='marker_image', full=True, null=True)

    class Meta:
        queryset = DateaFreeCategory.objects.all()
        resource_name = 'free_category'
        filtering={
                'name' : ALL
                }
