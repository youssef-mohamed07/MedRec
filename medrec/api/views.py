from rest_framework import generics, permissions, status, filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.db.models import Q
from .models import ImageUpload, Medicine
from .serializers import ImageUploadSerializer, MedicineSerializer, MedicineListSerializer
from core.ai_service import infer


class MedicineListView(generics.ListAPIView):
    """List all medicines with search and filter"""
    queryset = Medicine.objects.filter(is_active=True)
    serializer_class = MedicineListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'name_ar', 'name_en', 'scientific_name', 'category']
    ordering_fields = ['name_ar', 'name_en', 'price', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset


class MedicineDetailView(generics.RetrieveAPIView):
    """Get detailed medicine information"""
    queryset = Medicine.objects.filter(is_active=True)
    serializer_class = MedicineSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'code'


class MedicineSearchView(generics.ListAPIView):
    """Search medicines by code or name"""
    serializer_class = MedicineSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return Medicine.objects.filter(
                Q(code__icontains=query) |
                Q(name_ar__icontains=query) |
                Q(name_en__icontains=query) |
                Q(scientific_name__icontains=query) |
                Q(active_ingredients__icontains=query) |
                Q(alternatives__icontains=query)
            ).filter(is_active=True)[:20]
        return Medicine.objects.none()


class ImageUploadCreateView(generics.CreateAPIView):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(uploaded_by=request.user)

        # Run AI inference
        image_path = instance.image.path
        result = infer(image_path)
        
        # Save full result as JSON
        import json
        instance.result = json.dumps(result, ensure_ascii=False)
        instance.confidence = result.get('confidence', 0.0)
        
        # Try to match detected medicine by code
        medicine_code = result.get('medicine_code')
        if medicine_code:
            try:
                medicine = Medicine.objects.get(code=medicine_code, is_active=True)
                instance.detected_medicine = medicine
            except Medicine.DoesNotExist:
                pass
        
        instance.save()

        out_serializer = self.get_serializer(instance, context={'request': request})
        headers = self.get_success_headers(out_serializer.data)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ImageUploadListView(generics.ListAPIView):
    serializer_class = ImageUploadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ImageUpload.objects.filter(uploaded_by=self.request.user).order_by('-created_at')

class ImageUploadDetailView(generics.RetrieveDestroyAPIView):
    "`"`"Get or delete a specific upload/scan for the current user"`"`"
    serializer_class = ImageUploadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ImageUpload.objects.filter(uploaded_by=self.request.user)

class MedicineAlternativesView(generics.ListAPIView):
    "`"`"Find alternative medicines based on exact active ingredients"`"`"
    serializer_class = MedicineListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        code = self.kwargs.get('code')
        try:
            base_medicine = Medicine.objects.get(code=code, is_active=True)
            # Find others with the exact same active ingredients (excluding itself)
            if base_medicine.active_ingredients:
                return Medicine.objects.filter(
                    active_ingredients=base_medicine.active_ingredients,
                    is_active=True
                ).exclude(code=code)
            return Medicine.objects.none()
        except Medicine.DoesNotExist:
            return Medicine.objects.none()

class MedicineActiveIngredientsView(generics.ListAPIView):
    "`"`"Search medicines strictly by their active ingredients"`"`"
    serializer_class = MedicineListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        ingredient = self.kwargs.get('ingredient', '')
        if ingredient:
            return Medicine.objects.filter(
                active_ingredients__icontains=ingredient,
                is_active=True
            )
        return Medicine.objects.none()

class MedicineBySideEffectView(generics.ListAPIView):
    "`"`"Search medicines by side effects or warnings (e.g. check if a medicine causes drowsiness)"`"`"
    serializer_class = MedicineListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        effect = self.kwargs.get('effect', '')
        if effect:
            return Medicine.objects.filter(
                Q(side_effects__icontains=effect) | Q(warnings__icontains=effect),
                is_active=True
            )
        return Medicine.objects.none()

class MedicineByCategoryView(generics.ListAPIView):
    "`"`"Filter medicines strictly by a specific category (e.g. مسكنات, مضادات حيوية)"`"`"
    serializer_class = MedicineListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        category_name = self.kwargs.get('category', '')
        if category_name:
            return Medicine.objects.filter(
                category__icontains=category_name,
                is_active=True
            )
        return Medicine.objects.none()

class MedicineByManufacturerView(generics.ListAPIView):
    "`"`"Filter medicines strictly by Manufacturer/Company name"`"`"
    serializer_class = MedicineListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        manufacturer_name = self.kwargs.get('manufacturer', '')
        if manufacturer_name:
            return Medicine.objects.filter(
                manufacturer__icontains=manufacturer_name,
                is_active=True
            )
        return Medicine.objects.none()

class ClearUserScanHistoryView(generics.DestroyAPIView):
    "`"`"Wipes out the entire scan/upload history for the current user"`"`"
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ImageUpload.objects.filter(uploaded_by=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        count, _ = self.get_queryset().delete()
        return Response({"message": f"Successfully deleted {count} scan records."}, status=status.HTTP_204_NO_CONTENT)

class TopMedicinesView(generics.ListAPIView):
    "`"`"Returns a list of the 10 most recently added or updated medicines"`"`"
    serializer_class = MedicineListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Medicine.objects.filter(is_active=True).order_by('-created_at')[:10]
