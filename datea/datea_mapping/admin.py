
from django.contrib import admin
from olwidget.admin import GeoModelAdmin

from models import DateaMapping, DateaMapItem

class DateaMappingAdmin(GeoModelAdmin):
    model = DateaMapping
    maps = (
        (('center', 'boundary'), None),
    )

       
class DateaMapItemAdmin(GeoModelAdmin):
    model = DateaMapItem
    readonly_fields = ('vote_count', 'comment_count', 'reply_count', 'follow_count')


admin.site.register(DateaMapping, DateaMappingAdmin)
admin.site.register(DateaMapItem, DateaMapItemAdmin)