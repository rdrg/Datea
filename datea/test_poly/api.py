from tastypie.resources import ModelResource
from models import Meal, Salad

class MealResource(ModelResource):
    
    class Meta:
        queryset = Meal.objects.all()
        resource_name = 'meal'
        
class SaladResource(ModelResource):
    
    class Meta:
        queryset = Salad.objects.all()
        resource_name = 'salad'