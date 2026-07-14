from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config.admin_views import analytics, dashboard_context, management

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = "DJ Chemboi Admin"
admin.site.index_title = "Manage your brand"
admin.site.index_template = "admin/index.html"

_original_index = admin.site.index
def dashboard_index(request, extra_context=None):
    context = dashboard_context()
    if extra_context:
        context.update(extra_context)
    return _original_index(request, extra_context=context)
admin.site.index = dashboard_index

urlpatterns = [
    path("admin/analytics/", analytics, name="admin-analytics"),
    path("admin/management/", management, name="admin-management"),
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/", include("catalog.urls")),
    path("api/cart/", include("cart.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/bookings/", include("bookings.urls")),
    path("api/events/", include("events_app.urls")),
    path("api/gallery/", include("gallery.urls")),
    path("api/tracks/", include("music.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
