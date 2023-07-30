from django.contrib import admin

from .models import Product, ProductComment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'active']


@admin.register(ProductComment)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'author', 'text', 'stars', 'active']
