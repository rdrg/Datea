
from django.forms.widgets import SelectMultiple
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.encoding import force_unicode
from .models import DateaImage
from .forms import DateaImageForm
from django.template.loader import render_to_string
import logging


def get_new_image_form(field_name, visible=True, link_visible=False):
    return render_to_string('datea_images/new_image_form.html', 
                            {'form': DateaImageForm(), 
                             'field_name': field_name, 
                             'visible': visible,
                             'link_visible': link_visible})

def get_image_field(instance, context):
    return render_to_string('datea_images/image_field.html')
    

class DateaImageM2MWidget(SelectMultiple):
   
    def __init__(self, attrs=None, max_images=3, thumbnail_size="80x80", crop=None, **kwargs):
        
        super(DateaImageM2MWidget, self).__init__(attrs)
        
        self.max_images = max_images
        self.thumbnail_size = thumbnail_size
        self.crop = crop
    
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        final_attrs = self.build_attrs(attrs, name=name)
        

        image_objects=[]
        if len(value) > 0:
            image_objects = DateaImage.objects.filter(pk__in=value)
        
        form_visible = len(image_objects)==0
        if form_visible:
            link_visible = False
        else:
            if len(image_objects) < self.max_images:
                link_visible = True
            else:
                link_visible = False   
        nu_image_form = get_new_image_form(final_attrs['name'], form_visible, link_visible)
        
        crop = self.crop
        if self.crop == None:
            crop = ''
            
        context = {
                   "max_images": self.max_images,
                   "thumbnail_size": self.thumbnail_size,
                   "crop": crop,
                   "name": final_attrs['name'],
                   "css_id": final_attrs['id'],
                   "image_objects": image_objects,
                   "new_form": nu_image_form,
                   "num_values": len(value) 
                   }
        output = render_to_string("datea_images/field_wrap.html", context)

        return mark_safe(output)

    class Media:
        js = (#'js/jquery.ui.widget.js',
              #'js/jquery.iframe-transport.js',
              'datea/js/datea_images.js',)
        css = {
            'all': ('datea/css/datea_images.css',)
        }

