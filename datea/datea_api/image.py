from tastypie.resources import ModelResource
from datea.datea_image.models import DateaImage

class ImageResource(ModelResource):
    class Meta:
        queryset = DateaImage.objects.all()
        resource_name = 'image'
