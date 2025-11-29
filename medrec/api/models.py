from django.db import models
from django.contrib.auth.models import User


class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%m/%d')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    result = models.TextField(blank=True)  # JSON/text result from AI
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Upload {self.id} by {self.uploaded_by.username}'
