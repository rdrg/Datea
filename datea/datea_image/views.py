# Create your views here.
from models import DateaImage
from forms import ImageUploadForm
from django.utils import simplejson
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import Template, Context
from django.contrib.contenttypes.models import ContentType
from django.db.models import ForeignKey, ManyToManyField, OneToOneField 


def save_image(request):
    """
    Save DateaImage instance for specified object FK or M2M-Field
    post parameters must include:
        object_type:     name of the model class
        object_id:       pk of the instance
        object_field:    fk or m2m fieldname
        image:           image file input 
        order:           the order of the image (optional)
    """
    
    if not request.user.is_authenticated:
        return HttpResponse("<h1>Login required</h1>")
    
    form = ImageUploadForm(request.POST, request.FILES)

    if form.is_valid():
        
        # get model through content type, object instance, field class
        model = ContentType.objects.get(model=form.cleaned_data['object_type'].lower())
        object = model.get_object_for_this_type(pk=form.cleaned_data['object_id'])
        
        # Only access image if object is owned by user or user.is_staff
        # TODO: implement better permissions with something like django-guardian
        if object.user == request.user or request.user.is_staff:
            field_name = form.cleaned_data['object_field']
            field = object._meta.get_field(field_name)
            image_data = form.cleaned_data['image']
            
            # field is foreign key 
            if type(field) in [ForeignKey, OneToOneField]:
                image_instance = getattr(object, field_name)
                
                # create new DateaImage and save to objects foreignkey field 
                if not image_instance:
                    image_instance = DateaImage(image=image_data, user=request.user)
                    image_instance.save()
                    setattr(object, field_name, image_instance)
                    object.save()
                
                # update existing image 
                else:
                    image_instance.image = image_data
                    image_instance.save()
            
            elif type(field) == ManyToManyField:
                m2m = getattr(object, field_name)
                
                #if image_order specified, check if image exists
                if 'image_order' in request.POST and request.POST['image_order']:
                    order = request.POST['image_order']
                    # update existing image
                    try:
                        image_instance = m2m.get(order=order)
                        image_instance.image = image_data
                        image_instance.save()
                    # create new with specified order
                    except:
                        image_instance = DateaImage(image=image_data, user=request.user, order=order)
                        image_instance.save()
                        m2m.add(image_instance)
                
                # create new image with corresponding order (last + 1)
                else:
                    if m2m.count() == 0:
                        order = 0
                    else:
                        order = m2m.order_by('order')[0].order + 1
                    image_instance = DateaImage(image=image_data, user=request.user, order=order)
                    image_instance.save()
                    m2m.add(image_instance)    
                           
            data = simplejson.dumps({'ok': True, 'message':'Everything\'s fine'})
        else:
           data = simplejson.dumps({'ok': False, 'message': 'Permission denied'}) 
    else:
        data = simplejson.dumps({'ok': False, 'message': form.errors})
    
    context = Context({'data': data})
    tpl = Template('<textarea data-type="application/json">{{ data|safe }}</textarea>')
       
    return HttpResponse(tpl.render(context))
        
        
# CHECK THIS AGAIN LATER         
def delete_image(request, pk):
    """
    Delete DateaImage instance
    """
    try:
        instance = DateaImage.objects.get(pk=pk)
        instance.delete()
        
    except:
        pass
    
    
