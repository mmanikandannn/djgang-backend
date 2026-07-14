from rest_framework import permissions, viewsets

from .models import Track
from .serializers import TrackSerializer


class TrackViewSet(viewsets.ModelViewSet):
    serializer_class = TrackSerializer

    def get_queryset(self):
        qs = Track.objects.all()
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_published=True)
        return qs

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
