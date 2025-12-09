from django.contrib import admin
from .models import ImageUpload, Medicine


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('code', 'name_ar', 'name_en', 'category', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('code', 'name_ar', 'name_en', 'scientific_name', 'manufacturer')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name_ar', 'name_en', 'scientific_name', 'manufacturer', 'category')
        }),
        ('Details', {
            'fields': ('description_ar', 'description_en', 'dosage', 'price', 'image')
        }),
        ('Safety Information', {
            'fields': ('side_effects', 'warnings')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_by', 'detected_medicine', 'confidence', 'created_at', 'get_result_preview')
    list_filter = ('created_at', 'uploaded_by', 'detected_medicine')
    search_fields = ('uploaded_by__username', 'detected_medicine__name_ar', 'detected_medicine__code', 'result')
    readonly_fields = ('created_at', 'image_preview')
    
    def get_result_preview(self, obj):
        if obj.result:
            return obj.result[:50] + '...' if len(obj.result) > 50 else obj.result
        return '-'
    get_result_preview.short_description = 'Result Preview'
    
    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="max-height: 300px;"/>', obj.image.url)
        return '-'
    image_preview.short_description = 'Image Preview'
