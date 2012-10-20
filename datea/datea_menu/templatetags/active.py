from django import template

register = template.Library()

@register.simple_tag
def active_link(request, pattern):
    import re
    if re.search(str(pattern), request.path): 
        return 'navitem_active'
    else:
        return 'navitem' 