from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
# admin.site.register(Item)
# admin.site.register(Sub_Item)
admin.site.register(Cart)
# admin.site.register(Order)
admin.site.register(Book)

@admin.register(Sub_Item)
class SubAdmin(admin.ModelAdmin):
    list_display = ['subitem_name','price','size']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['item','quantity','deli']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name']


