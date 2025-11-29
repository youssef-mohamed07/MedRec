from django.contrib import admin
from .models import ImageUpload


@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_by', 'created_at', 'get_result_preview')
    list_filter = ('created_at', 'uploaded_by')
    search_fields = ('uploaded_by__username', 'result')
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
