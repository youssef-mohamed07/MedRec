from django.urls import path
from .views import ImageUploadCreateView, ImageUploadListView

urlpatterns = [
    path('uploads/', ImageUploadListView.as_view(), name='upload-list'),
    path('uploads/new/', ImageUploadCreateView.as_view(), name='upload-create'),
]
