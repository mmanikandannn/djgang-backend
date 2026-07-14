from rest_framework.routers import DefaultRouter

from .views import BookingEnquiryViewSet

router = DefaultRouter()
router.register("", BookingEnquiryViewSet, basename="booking")

urlpatterns = router.urls
