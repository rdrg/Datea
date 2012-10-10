# Create your views here.
import sys
from models import DateaImage
from forms import ImageUploadForm
from django.utils import simplejson
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import Template, Context
from django.contrib.contenttypes.models import ContentType
from django.db.models import ForeignKey, ManyToManyField, OneToOneField
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from datea.datea_api.image import ImageResource 
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
import cStringIO
from django.core.files.base import ContentFile

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
        
        # ADD DATEA IMAGE INSTANCE To EXISTING OBJECT
        if form.cleaned_data['object_id'] and form.cleaned_data['object_type'] and form.cleaned_data['object_field']:
        
            # get model through content type, object instance, field class
            model = ContentType.objects.get(model=form.cleaned_data['object_type'].lower())
            object = model.get_object_for_this_type(pk=form.cleaned_data['object_id'])
            
            # Only access image if object is owned by user or user.
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
                
                # create image resource
                ir = ImageResource()
                im_bundle = ir.build_bundle(obj=image_instance)
                im_bundle = ir.full_dehydrate(im_bundle)
                
                data = {'ok': True, 'message':'Everything\'s fine', 'resource': im_bundle.data }
                if form.cleaned_data['thumb_preset']:
                    try:
                        data['resource']['thumb'] = image_instance.get_thumb(form.cleaned_data['thumb_preset'])
                    except:
                        pass
                               
                data = simplejson.dumps(data)
            else:
                data = simplejson.dumps({'ok': False, 'message': 'Permission denied'})
        
        # JUST ADD IMAGE WITHOUT REFERENCING IT TO AN OBJECT
        else:
            image_data = form.cleaned_data['image']
            image_instance = DateaImage(image=image_data, user=request.user)
            if 'order' in form.cleaned_data:
                image_instance.order = form.cleaned_data['order']
            image_instance.save()
            
            # create image resource
            ir = ImageResource()
            im_bundle = ir.build_bundle(obj=image_instance)
            im_bundle = ir.full_dehydrate(im_bundle)
            
            data = {'ok': True, 'message':'Everything\'s fine', 'resource': im_bundle.data}
            if form.cleaned_data['thumb_preset']:
                    try:
                        data['resource']['thumb'] = image_instance.image[form.cleaned_data['thumb_preset']].url
                    except:
                        pass
            
            data = simplejson.dumps(data)
             
    else:
        data = simplejson.dumps({'ok': False, 'message': form.errors})
    
    context = Context({'data': data})
    tpl = Template('<textarea data-type="application/json">{{ data|safe }}</textarea>')
       
    return HttpResponse(tpl.render(context))
    
 
#@ensure_csrf_cookie
@csrf_exempt
def save_image_api(request):
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
    if request.method == 'POST' and request.FILES:
        print request.POST
        postdata = request.POST
        
        postfiles = request.FILES

    form = ImageUploadForm(request.POST, request.FILES)
    

    if form.is_valid():
        print "form valid"
        
        # ADD DATEA IMAGE INSTANCE To EXISTING OBJECT
        #if form.cleaned_data['object_id'] and form.cleaned_data['object_type'] and form.cleaned_data['object_field']:
        if postdata['object_id'] and postdata['object_type'] and postdata['object_field']:
        
            # get model through content type, object instance, field class
            model = ContentType.objects.get(model= postdata['object_type'].lower())
            object = model.get_object_for_this_type(pk=postdata['object_id'])
            
            # Only access image if object is owned by user or user.is_staff
            # TODO: implement better permissions with something like django-guardian
            if object.user == request.user or request.user.is_staff:
                field_name = postdata['object_field']
                field = object._meta.get_field(field_name)
                image_data = postfiles['image']
                
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
                
                # create image resource
                ir = ImageResource()
                im_bundle = ir.build_bundle(obj=image_instance)
                im_bundle = ir.full_dehydrate(im_bundle)
                
                data = {'ok': True, 'message':'Everything\'s fine', 'resource': im_bundle.data }
                if postdata['thumb_preset']:
                    try:
                        data['resource']['thumb'] = image_instance.get_thumb(postdata['thumb_preset'])
                    except:
                        pass
                               
                data = simplejson.dumps(data)
            else:
                data = simplejson.dumps({'ok': False, 'message': 'Permission denied'})
        
        # JUST ADD IMAGE WITHOUT REFERENCING IT TO AN OBJECT
        else:
            image_data = postdata['image']
            image_instance = DateaImage(image=image_data, user=request.user)
            if 'order' in form.cleaned_data:
                image_instance.order = form.cleaned_data['order']
            image_instance.save()
            
            # create image resource
            ir = ImageResource()
            im_bundle = ir.build_bundle(obj=image_instance)
            im_bundle = ir.full_dehydrate(im_bundle)
            
            data = {'ok': True, 'message':'Everything\'s fine', 'resource': im_bundle.data}
            if postdata['thumb_preset']:
                    try:
                        data['resource']['thumb'] = image_instance.image[postdata['thumb_preset']].url
                    except:
                        pass
            
            data = simplejson.dumps(data)
             
    else:
        data = simplejson.dumps({'ok': False, 'message': form.errors})
        print "form invalid"
        print form.errors

    context = Context({'data': data})
    tpl = Template('<textarea data-type="application/json">{{ data|safe }}</textarea>')
       
    return HttpResponse(tpl.render(context))
    
 
#@ensure_csrf_cookie
@csrf_exempt
def mobile_image_save(request):
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
    if request.method == 'POST':
        print request.POST
        if request.POST.get('file'):
            #print('got file field')
            file = ContentFile(base64.b64decode(request.POST.get('file')))
            #file = cStringIO.StringIO(base64.b64decode(request.POST.get('file')))
            image = InMemoryUploadedFile(file,
                field_name = 'file',
                name = "generic.jpg",
                content_type="image/jpeg",
                size = sys.getsizeof(file),
                charset=None)
            request.FILES[u'image'] = image
            print "posted files: ", request.FILES

        postdata = request.POST
        
        postfiles = request.FILES

    form = ImageUploadForm(request.POST, request.FILES)
    
    if form.is_valid():
        print "form valid"
        
        # ADD DATEA IMAGE INSTANCE To EXISTING OBJECT
        #if form.cleaned_data['object_id'] and form.cleaned_data['object_type'] and form.cleaned_data['object_field']:
        if postdata['object_id'] and postdata['object_type'] and postdata['object_field']:
        
            # get model through content type, object instance, field class
            model = ContentType.objects.get(model= postdata['object_type'].lower())
            object = model.get_object_for_this_type(pk=postdata['object_id'])
            
            # Only access image if object is owned by user or user.is_staff
            # TODO: implement better permissions with something like django-guardian
            if object.user == request.user or request.user.is_staff:
                field_name = postdata['object_field']
                field = object._meta.get_field(field_name)
                image_data = postfiles['image']
                
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
                
                # create image resource
                ir = ImageResource()
                im_bundle = ir.build_bundle(obj=image_instance)
                im_bundle = ir.full_dehydrate(im_bundle)
                
                data = {'ok': True, 'message':'Everything\'s fine', 'resource': im_bundle.data }
                if postdata['thumb_preset']:
                    try:
                        data['resource']['thumb'] = image_instance.get_thumb(postdata['thumb_preset'])
                    except:
                        pass
                               
                data = simplejson.dumps(data)
            else:
                data = simplejson.dumps({'ok': False, 'message': 'Permission denied'})
        
        # JUST ADD IMAGE WITHOUT REFERENCING IT TO AN OBJECT
        else:
            image_data = postdata['image']
            image_instance = DateaImage(image=image_data, user=request.user)
            if 'order' in form.cleaned_data:
                image_instance.order = form.cleaned_data['order']
            image_instance.save()
            
            # create image resource
            ir = ImageResource()
            im_bundle = ir.build_bundle(obj=image_instance)
            im_bundle = ir.full_dehydrate(im_bundle)
            
            data = {'ok': True, 'message':'Everything\'s fine', 'resource': im_bundle.data}
            if postdata['thumb_preset']:
                    try:
                        data['resource']['thumb'] = image_instance.image[postdata['thumb_preset']].url
                    except:
                        pass
            
            data = simplejson.dumps(data)
             
    else:
        data = simplejson.dumps({'ok': False, 'message': form.errors})
        print "form invalid"
        print form.errors

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
    
    
