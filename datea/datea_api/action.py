from tastypie import fields
from tastypie.resources import ModelResource
from datea.datea_action.models import DateaAction
from tastypie.cache import SimpleCache

class ActionResource(ModelResource):
    category = fields.ToOneField('datea.datea_api.category.CategoryResource',
            attribute='category', null=True, full=True, readonly=True)
    
    class Meta:
        queryset = DateaAction.objects.all()
        resource_name = 'action'
        allowed_methods = ['get']
        cache = SimpleCache(timeout=10)