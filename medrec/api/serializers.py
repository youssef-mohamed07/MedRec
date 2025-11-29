from rest_framework import serializers
from .models import ImageUpload


class ImageUploadSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ImageUpload
        fields = ('id', 'image', 'image_url', 'result', 'created_at')
        read_only_fields = ('result', 'created_at')

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
