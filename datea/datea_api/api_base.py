from tastypie.bundle import Bundle
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.contrib.gis.resources import ModelResource as GeoModelResource
from django.contrib.gis.geos import Point


# Api key + web authentication
# taken from https://github.com/toastdriven/django-tastypie/issues/197
class ApiKeyPlusWebAuthentication(ApiKeyAuthentication):
    
    def is_authenticated(self, request, **kwargs):
        if request.user.is_authenticated() or request.method == 'GET':
            return True

        return super(ApiKeyPlusWebAuthentication, self).is_authenticated(request, **kwargs)

    def get_identifier(self, request):
        if request.user.is_authenticated():
            return request.user.username
        else:
            return super(ApiKeyPlusWebAuthentication, self).get_identifier(request)


# Base Authorization
# derived from http://blog.gingerlime.com/keep-your-hands-off-my-tastypie/
class DateaBaseAuthorization(Authorization):
    '''
    Per object authorization:
        - read: all allowed
        - update/put: is_staff / object owner
        - delete: is_staff / object owner
    '''
    
    def apply_limits(self, request, object_list=None):
        
        if request and request.method == 'GET':
            return object_list
        
        if request and request.method == 'DELETE':
            return object_list.filter(user=request.user)
 
        if isinstance(object_list, Bundle):
            return object_list
            bundle = object_list # for clarity, lets call it a bundle
            bundle.data['user'] = {'pk': request.user.pk }  # ensure user data is not manipulated - chequear bien esto
            
            #if request.method == 'PUT':
            #    print vars(bundle.obj)
            
            return bundle
 
        return []
    
    

class DateaBaseResource(ModelResource):
 
    def obj_create(self, bundle, request, **kwargs):  # 5.
        bundle = self._meta.authorization.apply_limits(request, bundle)
        return super(DateaBaseResource, self).obj_create(bundle, request, user=request.user)
 
    def obj_update(self, bundle, request, **kwargs):  # 6.
        bundle = self._meta.authorization.apply_limits(request, bundle)
        return super(DateaBaseResource, self).obj_update(bundle, request, user=request.user)
    


# GeoModelResource with distance sorting: https://gist.github.com/1551309
class DateaBaseGeoResource(GeoModelResource):
 
    def obj_create(self, bundle, request, **kwargs):  # 5.
        bundle = self._meta.authorization.apply_limits(request, bundle)
        return super(DateaBaseGeoResource, self).obj_create(bundle, request, **kwargs)
 
    def obj_update(self, bundle, request, **kwargs):  # 6.
        bundle = self._meta.authorization.apply_limits(request, bundle)
        return super(DateaBaseGeoResource, self).obj_update(bundle, request, **kwargs)
    
    
    def apply_sorting(self, objects, options=None):
        if options and "longitude" in options and "latitude" in options:
            return objects.distance(Point(options['latitude'], options['longitude'])).order_by('distance')

        return super(DateaBaseGeoResource, self).apply_sorting(objects, options)
    
    
