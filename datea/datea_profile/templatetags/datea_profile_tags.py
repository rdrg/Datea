
from django import template
import re

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

