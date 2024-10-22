from django.contrib import admin
from .models import *
from customer.models import Review

# Register your models here.

# import all modules from .models

class ProductImageInline(admin.TabularInline):
    model=ProductImage
    readonly_fields=['image_tag']
    extra=1

class ReviewInLine(admin.TabularInline):
    model=Review
    readonly_fields=['customer','star_count','comment']
    extra=0 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductImageInline, ReviewInLine]
               


admin.site.register(Campaign) 
admin.site.register(GeneralCategory) 
admin.site.register(Category) 
admin.site.register(Size) 
admin.site.register(Color) 
admin.site.register(ProductImage)

