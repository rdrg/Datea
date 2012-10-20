from tastypie.resources import ModelResource
from datea.datea_image.models import DateaImage
from api_base import ApiKeyPlusWebAuthentication, DateaBaseAuthorization, DateaBaseResource

class ImageResource(DateaBaseResource):
    
    def dehydrate(self, bundle):
        bundle.data['thumb'] = bundle.obj.get_thumb()
        bundle.data['image'] = bundle.obj.get_thumb('image_thumb_large')
        return bundle
    
    def hydrate(self, bundle):
        # images are not to be updated here: this overrides the process for foreignkey fields
        if 'id' in bundle.data:
            bundle.obj = DateaImage.objects.get(pk=bundle.data['id'])
        return bundle
    
    class Meta:
        queryset = DateaImage.objects.all()
        resource_name = 'image'
        allowed_methods = ['get', 'delete']
        authentication = ApiKeyPlusWebAuthentication()
        authorization = DateaBaseAuthorization()
