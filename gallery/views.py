from rest_framework import permissions, viewsets

from .models import GalleryImage
from .serializers import GalleryImageSerializer


class GalleryImageViewSet(viewsets.ModelViewSet):
    serializer_class = GalleryImageSerializer

    def get_queryset(self):
        qs = GalleryImage.objects.all()
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_published=True)
        return qs

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
