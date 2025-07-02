from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount', 'stock', 'is_featured', 'created_at']
    list_filter = ['category', 'is_featured', 'created_at']
    list_editable = ['price', 'discount', 'stock', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'discount')
        }),
        ('Inventory', {
            'fields': ('stock', 'is_featured')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('created_at', 'updated_at')
        return ()
