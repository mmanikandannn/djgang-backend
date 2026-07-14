from rest_framework.routers import DefaultRouter

from .views import GalleryImageViewSet

router = DefaultRouter()
router.register("", GalleryImageViewSet, basename="gallery-image")

urlpatterns = router.urls
