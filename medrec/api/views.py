from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import ImageUpload
from .serializers import ImageUploadSerializer
from core.ai_service import infer


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

        # run AI inference (placeholder)
        image_path = instance.image.path
        result = infer(image_path)
        instance.result = str(result)
        instance.save()

        out_serializer = self.get_serializer(instance, context={'request': request})
        headers = self.get_success_headers(out_serializer.data)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ImageUploadListView(generics.ListAPIView):
    serializer_class = ImageUploadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ImageUpload.objects.filter(uploaded_by=self.request.user).order_by('-created_at')
