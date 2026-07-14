from rest_framework import mixins, permissions, viewsets

from .models import BookingEnquiry
from .serializers import BookingEnquirySerializer


class BookingEnquiryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                             mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    POST /api/bookings/         -> public: submit a booking enquiry (no login needed)
    GET  /api/bookings/         -> staff only: list all enquiries
    """

    queryset = BookingEnquiry.objects.all()
    serializer_class = BookingEnquirySerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
