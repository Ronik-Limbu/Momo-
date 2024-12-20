from django.contrib import admin
from .models import Foods,Category
@admin.register(Foods)
class FoodsAdmin(admin.ModelAdmin):
    list_display=['id','name','image','price','desc','category']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name'] 


