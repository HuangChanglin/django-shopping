from django.contrib import admin
from .models import Category, Product, ProductImage, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'sort', 'is_active', 'created_at']
    list_filter = ['is_active', 'parent']
    search_fields = ['name']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'sales', 'status', 'is_hot', 'is_recommended']
    list_filter = ['status', 'is_hot', 'is_recommended', 'category']
    search_fields = ['name', 'description']
    list_editable = ['status', 'is_hot', 'is_recommended']
    inlines = [ProductImageInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_anonymous', 'created_at']
    list_filter = ['rating', 'is_anonymous']
    search_fields = ['content']
