from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create', 'update')
    list_filter = ('create',)
    prepopulated_fields = {
        'slug': ('name',)
    }
admin.site.register(Category, CategoryAdmin )



class CastomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'password',)
    list_filter = ('first_name', 'last_name')
admin.site.register(Castomer, CastomerAdmin),



class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount','unit_price','discount','total_price','create',
                    'update', 'available', 'description', 'image')
    list_filter = ('available',)
admin.site.register(Product, ProductAdmin),



class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'quantity', 'price', 'address',
                    'phone', 'date', 'status', )
    list_filter = ('product', 'customer')
admin.site.register(Order, OrderAdmin),