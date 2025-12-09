from django.db import models
from django.contrib.auth.models import User


class Medicine(models.Model):
    """Medicine catalog with codes and details"""
    code = models.CharField(max_length=50, unique=True, db_index=True)
    name_ar = models.CharField(max_length=200, help_text="الاسم بالعربي")
    name_en = models.CharField(max_length=200, help_text="English name")
    scientific_name = models.CharField(max_length=200, blank=True)
    manufacturer = models.CharField(max_length=200, blank=True)
    description_ar = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    dosage = models.CharField(max_length=200, blank=True, help_text="الجرعة")
    side_effects = models.TextField(blank=True, help_text="الآثار الجانبية")
    warnings = models.TextField(blank=True, help_text="التحذيرات")
    category = models.CharField(max_length=100, blank=True, help_text="تصنيف الدواء")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='medicines/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name_ar']
        verbose_name = 'Medicine'
        verbose_name_plural = 'Medicines'

    def __str__(self):
        return f"{self.code} - {self.name_ar}"


class ImageUpload(models.Model):
    """User uploaded images for medicine detection"""
    image = models.ImageField(upload_to='uploads/%Y/%m/%d')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    detected_medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True, blank=True, related_name='detections')
    confidence = models.FloatField(null=True, blank=True, help_text="AI confidence score")
    result = models.TextField(blank=True)  # Full JSON result from AI
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Upload {self.id} by {self.uploaded_by.username}'
