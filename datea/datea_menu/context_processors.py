from datea.datea_menu.models import Item

def menu_items(request):
    menu=Item.objects.all().filter(visible=True).order_by('order')
       
    return {'datea_menu': menu}

