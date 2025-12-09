from django.urls import path
from .views import (
    ImageUploadCreateView,
    ImageUploadListView,
    MedicineListView,
    MedicineDetailView,
    MedicineSearchView
)

urlpatterns = [
    # Image uploads
    path('uploads/', ImageUploadListView.as_view(), name='upload-list'),
    path('uploads/new/', ImageUploadCreateView.as_view(), name='upload-create'),
    
    # Medicines
    path('medicines/', MedicineListView.as_view(), name='medicine-list'),
    path('medicines/search/', MedicineSearchView.as_view(), name='medicine-search'),
    path('medicines/<str:code>/', MedicineDetailView.as_view(), name='medicine-detail'),
]
