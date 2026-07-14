from datetime import date, timedelta

from django.core.management.base import BaseCommand

from catalog.models import Category, Product
from events_app.models import Event
from music.models import Track


class Command(BaseCommand):
    help = "Seeds demo categories, products, events, and tracks matching the frontend mock data."

    def handle(self, *args, **options):
        categories = {
            "T-Shirts": "Graphic tees for the front row.",
            "Oversized Tees": "Drop-shoulder streetwear fits.",
            "Hoodies": "Heavyweight fleece for cold festival nights.",
            "Caps": "Structured caps with embroidered logos.",
            "Stickers": "Die-cut holographic pack.",
            "Posters": "Museum-grade tour art prints.",
            "Event Passes": "VIP and general admission passes.",
            "Digital Mixes": "Instant-download DJ sets.",
        }
        cat_objs = {}
        for name, desc in categories.items():
            cat, _ = Category.objects.get_or_create(name=name, defaults={"description": desc})
            cat_objs[name] = cat
        self.stdout.write(self.style.SUCCESS(f"Categories ready: {len(cat_objs)}"))

        products = [
            ("Neon Skull Tee", "T-Shirts", 1299, 1599, ["S", "M", "L", "XL"], 14, "Bestseller"),
            ("VOID Oversized Tee", "Oversized Tees", 1499, None, ["M", "L", "XL", "XXL"], 9, "New"),
            ("Dark Energy Hoodie", "Hoodies", 2799, 3199, ["S", "M", "L", "XL", "XXL"], 6, "Bestseller"),
            ("Cyan Strike Cap", "Caps", 899, None, ["ONE_SIZE"], 20, ""),
            ("Neon Nights Sticker Pack", "Stickers", 249, None, ["ONE_SIZE"], 60, ""),
            ("Hi-Tech Tour Poster", "Posters", 599, None, ["A3", "A2"], 25, ""),
            ("Festival VIP Pass", "Event Passes", 4999, None, ["ONE_SIZE"], 40, "Limited"),
        ]
        for name, cat_name, price, compare_at, sizes, stock, tag in products:
            Product.objects.get_or_create(
                name=name,
                defaults=dict(
                    category=cat_objs[cat_name], price=price, compare_at_price=compare_at,
                    sizes=sizes, stock=stock, tag=tag, is_active=True,
                ),
            )
        Product.objects.get_or_create(
            name="Psytrance Sessions Vol.4 (Digital)",
            defaults=dict(
                category=cat_objs["Digital Mixes"], price=349, sizes=["MP3", "WAV"],
                stock=999, is_digital=True, tag="Digital", is_active=True,
            ),
        )
        self.stdout.write(self.style.SUCCESS(f"Products ready: {Product.objects.count()}"))

        events = [
            ("Neon Nights Festival", "Psytrance / Hi-Tech", "Vagator Beach Arena", "Goa", 40, Event.Status.AVAILABLE),
            ("Dark Energy Warehouse", "Techno", "The Foundry", "Mumbai", 60, Event.Status.SELLING_FAST),
            ("Melodic Skies Rooftop", "Melodic Techno", "Skyline Terrace", "Bangalore", 83, Event.Status.AVAILABLE),
            ("Future Sound Arena Tour", "EDM", "NSIC Grounds", "Delhi", 104, Event.Status.SOLD_OUT),
        ]
        for title, genre, venue, city, days_ahead, status in events:
            Event.objects.get_or_create(
                title=title,
                defaults=dict(genre=genre, venue=venue, city=city, date=date.today() + timedelta(days=days_ahead), status=status),
            )
        self.stdout.write(self.style.SUCCESS(f"Events ready: {Event.objects.count()}"))

        tracks = [
            ("Psytrance Sessions Vol.4", Track.Genre.PSYTRANCE, "80:00"),
            ("Hi-Tech Warehouse Set", Track.Genre.HITECH, "62:15"),
            ("Melodic Skies Live", Track.Genre.MELODIC_TECHNO, "58:20"),
        ]
        for title, genre, duration in tracks:
            Track.objects.get_or_create(title=title, defaults=dict(genre=genre, duration=duration))
        self.stdout.write(self.style.SUCCESS(f"Tracks ready: {Track.objects.count()}"))

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
