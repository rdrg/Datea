from django import template
from datea.datea_menu.models import DateaMenuItem

register = template.Library()

@register.assignment_tag
def get_menu(menu_root_id):
    try:
        root = DateaMenuItem.objects.get(menu_root_id=menu_root_id)
        items = list(root.get_children().filter(visible=True))
    except:
        items = []
    
    for i in items:
        if i.page:
            i.url = i.page.url
        elif i.external_url:
            i.url = i.external_url
        else:
            i.url = ''
        
    return items