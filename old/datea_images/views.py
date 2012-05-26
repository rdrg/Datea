from forms import DateaImageForm
from models import DateaImage
from django.template.loader import render_to_string
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response
from sorl.thumbnail import get_thumbnail
from django.conf import settings
import os

import mimetypes

def save_image(request):
    
    form = DateaImageForm(request.POST, request.FILES)
    if form.is_valid():
        image = form.save(commit=False)
        image.author = request.user
        image.save()
        crop = request.POST['crop']
        context = {
                   'thumbnail_size': request.POST['thumbnail_size'],
                   'name': request.POST['field_name'], 
                   'image' : image,
                   'crop': crop, 
                   }
        response = render_to_string("datea_images/image_field_ajax.html", context)
    else:
        response = ",".join(form.errors)
    
    return HttpResponse(response)
  
    
def delete_image(request, pk):
    
    try:
        image = DateaImage.objects.get(pk=pk)
        image.delete()
        msg = 'success'
    except:
        msg = 'error'
        pass
    
    return HttpResponse(mark_safe(msg), mimetype='text/plain')


def show_image(request, size, pk):
    image_inst = DateaImage.objects.get(pk=pk)
    thumb = get_thumbnail(image_inst.image.path, size, quality=90)
    thumb_path = os.path.join(settings.MEDIA_ROOT, thumb.name)
    img_data = open(thumb_path, "rb").read()
    mtype = mimetypes.guess_type(thumb_path)[0]
    return HttpResponse(img_data, mimetype=mtype)
    
