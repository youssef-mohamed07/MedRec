from rest_framework import serializers
from .models import ImageUpload, Medicine


class MedicineSerializer(serializers.ModelSerializer):
    """Serializer for Medicine model"""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Medicine
        fields = (
            'id', 'code', 'name_ar', 'name_en', 'scientific_name',
            'manufacturer', 'description_ar', 'description_en',
            'dosage', 'side_effects', 'warnings', 'category',
            'price', 'image', 'image_url', 'is_active',
            'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class MedicineListSerializer(serializers.ModelSerializer):
    """Simplified serializer for medicine listing"""
    class Meta:
        model = Medicine
        fields = ('id', 'code', 'name_ar', 'name_en', 'category', 'price')


class ImageUploadSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    medicine_details = MedicineSerializer(source='detected_medicine', read_only=True)

    class Meta:
        model = ImageUpload
        fields = (
            'id', 'image', 'image_url', 'detected_medicine',
            'medicine_details', 'confidence', 'result', 'created_at'
        )
        read_only_fields = ('detected_medicine', 'confidence', 'result', 'created_at')

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
