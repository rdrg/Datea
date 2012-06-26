
from django import template
import re
from datea.datea_api.profile import UserResource
from django.utils import simplejson
from django.utils.translation import ugettext as _
from datea.datea_image.utils import get_image_thumb
from django.conf import settings

register = template.Library()


# revisar! ->copiado deproyecto anterior

@register.simple_tag(takes_context=True)
def get_login_target(context):
    
    target = '/'
    request = context['request']
    if 'next' in request.GET:
        target = request.GET['next']
    
    referer = request.META.get('HTTP_REFERER', None)
    if referer:
        referer = referer.split('?')[0]
        referer = re.sub('^https?:\/\/', '', referer).split('/')
        if referer[0] == request.META.get('HTTP_HOST') and len(referer) > 1:
            target = "/"+"/".join(referer[1:])
    
    if target in ['/account/login/','/account/signup/', '/account/password_reset/', '/accounts/logout/','/', '']:
        target = '/'
        
    return target



@register.simple_tag(takes_context=True)
def get_user_resource(context):
    
    request = context['request']
    
    if request.user.is_authenticated():
        user_rsc = UserResource()
        user_bundle = user_rsc.build_bundle(obj=request.user)
        user_bundle = user_rsc.full_dehydrate(user_bundle)
        if request.user.is_staff:
            user_bundle.data['is_staff'] = True
        user_json = user_rsc.serialize(None, user_bundle, 'application/json')
        
    else:
        img_url = settings.DEFAULT_PROFILE_IMAGE
        user_data = {
            'username': _('anonimous'),
            'profile': {
                'image_small': get_image_thumb(img_url, 'profile_image_small').url,
                'image': get_image_thumb(img_url, 'profile_image').url,
                'image_large': get_image_thumb(img_url, 'profile_image_large').url,
            }
        }
        user_json = simplejson.dumps(user_data)
    return user_json


