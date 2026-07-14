"""
Seeds the "Pendants" shop category with the 17 gold pendant designs supplied by
the store owner. Each product gets a main listing image plus a 3-image gallery
(front / detail / lifestyle angle) so the product page has a working carousel.

NOTE: Only one product photo was supplied per design, so all 3 gallery slots
currently point at that same photo (just labelled differently). Swap in real
side/back/lifestyle shots later from Django admin -> Products -> (pick
product) -> Gallery images, or by re-running this command after replacing the
files in backend/seed_images/pendants/.

Usage:
    python manage.py seed_pendant_products
    python manage.py seed_pendant_products --reset   # wipe & reseed this category only
"""

import os

from django.core.files import File
from django.core.management.base import BaseCommand

from catalog.models import Category, Product, ProductImage

SEED_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "..", "seed_images", "pendants")
SEED_DIR = os.path.normpath(SEED_DIR)

CATEGORY_NAME = "Pendants"
CATEGORY_DESC = "Handcrafted gold-finish pendants and statement charms."

# (filename stem, product name, short description, price, tag)
# price is set within the requested 299-499 range; change anytime in Django
# admin or by editing this list and re-running the command.
PENDANTS = [
    ("floral-crescent-pendant", "Floral Crescent Statement Pendant",
     "Bold crescent hoop framed with delicate beaded floral filigree.", 449, "Bestseller"),
    ("reversible-smiley-pendant", "Reversible Mood Smiley Pendant",
     "Flip-face happy/sad charm cut from polished gold-tone metal.", 299, "New"),
    ("flower-of-life-pendant", "Flower of Life Sacred Geometry Pendant",
     "Classic sacred-geometry disc with a brushed-gold finish.", 349, ""),
    ("buddha-lotus-mandala-pendant", "Buddha Lotus Mandala Pendant",
     "Meditating Buddha silhouette framed by a radiant lotus mandala.", 479, "Bestseller"),
    ("buddha-head-pendant", "Buddha Head Pendant",
     "Sculptural Buddha head pendant with fine detailing and antique finish.", 459, ""),
    ("tree-of-life-round-pendant", "Tree of Life Round Pendant",
     "Classic leafy Tree of Life medallion in polished gold tone.", 329, ""),
    ("om-tree-of-life-pendant", "Om Tree of Life Pendant",
     "Tree of Life roots and branches wrapped around a carved Om symbol.", 399, "New"),
    ("rampant-lion-crest-pendant", "Rampant Lion Crest Pendant",
     "Heraldic roaring lion pendant with intricate mane and tail detail.", 499, "Limited"),
    ("yggdrasil-rune-tree-pendant", "Yggdrasil Norse Rune Tree Pendant",
     "Celtic-knot Tree of Life pendant ringed with Elder Futhark runes.", 469, "Bestseller"),
    ("teardrop-netted-swirl-pendant", "Teardrop Netted Swirl Pendant",
     "Teardrop pendant with an openwork net pattern and spiral accent.", 359, ""),
    ("triangle-trinity-amulet-pendant", "Triangle Trinity Amulet Pendant",
     "Geometric trinity amulet with beaded sunburst detailing.", 379, ""),
    ("three-headed-dragon-crest-pendant", "Three-Headed Dragon Crest Pendant",
     "Fantasy-inspired three-headed dragon crest pendant, fully sculpted.", 499, "Limited"),
    ("tree-of-life-branch-pendant", "Tree of Life Branch Pendant",
     "Slim branching Tree of Life pendant in a modern linear style.", 309, ""),
    ("star-tetrahedron-merkaba-pendant", "Star Tetrahedron Merkaba Pendant",
     "Six-pointed Merkaba star with layered sacred-geometry filigree.", 489, "New"),
    ("native-chief-headdress-pendant", "Native Chief Headdress Pendant",
     "Detailed profile pendant with a full feathered headdress.", 459, ""),
    ("cursive-initial-e-pendant", "Cursive Initial \"E\" Pendant",
     "Sculptural high-polish cursive letter pendant.", 319, ""),
    ("beaded-halo-circle-pendant", "Beaded Halo Circle Pendant",
     "Open circle pendant edged with graduated polished gold beads.", 339, ""),
]

GALLERY_LABELS = ["Front view", "Detail view", "Lifestyle view"]


class Command(BaseCommand):
    help = "Seeds the Pendants shop category with 17 gold pendant products (3 gallery images each)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing products in the Pendants category before reseeding.",
        )

    def handle(self, *args, **options):
        category, _ = Category.objects.get_or_create(
            name=CATEGORY_NAME, defaults={"description": CATEGORY_DESC}
        )

        if options["reset"]:
            deleted, _ = Product.objects.filter(category=category).delete()
            self.stdout.write(self.style.WARNING(f"Removed existing Pendants products ({deleted} rows)."))

        if not os.path.isdir(SEED_DIR):
            self.stderr.write(self.style.ERROR(f"Seed image folder not found: {SEED_DIR}"))
            return

        created_count = 0
        for stem, name, desc, price, tag in PENDANTS:
            image_path = os.path.join(SEED_DIR, f"{stem}.jpeg")
            if not os.path.exists(image_path):
                self.stderr.write(self.style.WARNING(f"Missing image for {name}: {image_path}"))
                continue

            product, created = Product.objects.get_or_create(
                name=name,
                defaults=dict(
                    category=category,
                    description=desc,
                    price=price,
                    sizes=["ONE_SIZE"],
                    stock=15,
                    tag=tag,
                    is_active=True,
                ),
            )

            # Set/refresh the main product image
            with open(image_path, "rb") as f:
                product.image.save(f"{stem}.jpeg", File(f), save=True)

            # Only (re)build the gallery if it's empty, so re-running the
            # command doesn't keep duplicating images.
            if not product.gallery_images.exists():
                for order, label in enumerate(GALLERY_LABELS):
                    with open(image_path, "rb") as f:
                        gallery_image = ProductImage(
                            product=product, alt_text=f"{name} - {label}", order=order
                        )
                        gallery_image.image.save(f"{stem}-{order+1}.jpeg", File(f), save=True)

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {name} (₹{price})"))
            else:
                self.stdout.write(f"Updated images for existing product: {name}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. {created_count} new pendant products created. "
                f"Category '{CATEGORY_NAME}' now has {category.products.count()} products."
            )
        )
