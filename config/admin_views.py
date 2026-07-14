from datetime import timedelta
from decimal import Decimal

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.shortcuts import render
from django.utils import timezone

from bookings.models import BookingEnquiry
from catalog.models import Category, Product
from events_app.models import Event
from gallery.models import GalleryImage
from music.models import Track
from orders.models import Order


def dashboard_context():
    now = timezone.now()
    today = timezone.localdate()
    month_start = now - timedelta(days=30)
    User = get_user_model()

    paid = Order.objects.filter(is_paid=True)
    revenue = paid.aggregate(value=Sum("total"))["value"] or Decimal("0")
    order_count = Order.objects.count()

    return {
        "total_users": User.objects.count(),
        "new_users": User.objects.filter(date_joined__gte=month_start).count(),
        "active_users": User.objects.filter(is_active=True).count(),
        "total_bookings": BookingEnquiry.objects.count(),
        "pending_bookings": BookingEnquiry.objects.filter(status=BookingEnquiry.Status.NEW).count(),
        "confirmed_bookings": BookingEnquiry.objects.filter(status=BookingEnquiry.Status.CONFIRMED).count(),
        "upcoming_events": Event.objects.filter(date__gte=today, is_published=True).count(),
        "total_orders": order_count,
        "paid_orders": paid.count(),
        "pending_orders": Order.objects.filter(status=Order.Status.PENDING).count(),
        "revenue": revenue,
        "average_order": (revenue / paid.count()) if paid.count() else Decimal("0"),
        "products": Product.objects.count(),
        "low_stock": Product.objects.filter(is_digital=False, stock__lt=5, is_active=True).count(),
        "tracks": Track.objects.count(),
        "gallery_items": GalleryImage.objects.count(),
        "events": Event.objects.count(),
        "categories": Category.objects.count(),
        "recent_bookings": BookingEnquiry.objects.all()[:6],
        "recent_orders": Order.objects.select_related("user").all()[:6],
        "recent_users": User.objects.order_by("-date_joined")[:6],
        "next_events": Event.objects.filter(date__gte=today).order_by("date")[:6],
    }


@staff_member_required
def analytics(request):
    context = dashboard_context()
    context.update({
        "title": "Analytics",
        "order_statuses": Order.objects.values("status").annotate(total=Count("id")).order_by("status"),
        "booking_statuses": BookingEnquiry.objects.values("status").annotate(total=Count("id")).order_by("status"),
        "top_products": Product.objects.annotate(order_count=Count("orderitem")).order_by("-order_count", "name")[:10],
    })
    return render(request, "admin/analytics.html", context)


@staff_member_required
def management(request):
    context = dashboard_context()
    context["title"] = "Management"
    return render(request, "admin/management.html", context)
