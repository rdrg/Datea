from django.contrib import admin
from models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'order', 'visible')
    list_editable = ['order']


admin.site.register(Item,ItemAdmin)


