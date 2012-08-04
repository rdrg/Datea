from django.contrib import admin
from models import Item, DateaMenuItem
from mptt.admin import MPTTModelAdmin

#class ItemAdmin(admin.ModelAdmin):
#    list_display = ('name', 'url', 'order', 'visible')
#    list_editable = ['order']
    
#admin.site.register(Item,ItemAdmin)


class CustomMPTTModelAdmin(MPTTModelAdmin):
    # speficfy pixel amount for this ModelAdmin only:
    mptt_level_indent = 35
admin.site.register(DateaMenuItem, CustomMPTTModelAdmin)


