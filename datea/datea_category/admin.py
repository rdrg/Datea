from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from models import DateaCategory, DateaFreeCategory

admin.site.register(DateaCategory,MPTTModelAdmin)
admin.site.register(DateaFreeCategory)