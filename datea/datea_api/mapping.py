from tastypie import fields
#from tastypie.resources import ModelResource
#from tastypie.contrib.gis.resources import ModelResource
from datea.datea_mapping.models import DateaMapping, DateaMapItem
from datea.datea_api.category import FreeCategoryResource
from api_base import ApiKeyPlusWebAuthentication, DateaBaseAuthorization, DateaBaseGeoResource


class MappingResource(DateaBaseGeoResource):
    
    user = fields.ToOneField('datea.datea_api.profile.UserResource', 
            attribute='user', full=True)
    item_category = fields.ToManyField('datea.datea_api.category.FreeCategoryResource', 
            attribute = 'item_categories', full=True, null=True)
  
    class Meta:
        queryset = DateaMapping.objects.all()
        resource_name = 'mapping'
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DateaBaseAuthorization()


        
class MapItemResource(DateaBaseGeoResource):
    
    category = fields.ToOneField('datea.datea_api.category.FreeCategoryResource',
            attribute= 'category', null=True, full=True)
    image = fields.ToManyField('datea.datea_api.image.ImageResource',
            attribute='images', null=True, full=True)
    mapping = fields.ToOneField('datea.datea_api.mapping.MappingResource',
            attribute='mapping', null=True, full=True)

    class Meta:
        queryset = DateaMapItem.objects.all()
        resource_name = 'map_item'
        allowed_methods = ['get','post','put','delete']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DateaBaseAuthorization()


