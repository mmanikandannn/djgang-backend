from rest_framework import serializers

from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(source="products.count", read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "image", "is_active", "product_count"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text", "order"]


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    category_slug = serializers.SlugRelatedField(source="category", slug_field="slug", read_only=True)
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "category", "category_slug", "price", "compare_at_price",
            "sizes", "stock", "in_stock", "is_digital", "image", "tag", "rating",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category", queryset=Category.objects.all(), write_only=True
    )
    gallery_images = ProductImageSerializer(many=True, read_only=True)
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "category", "category_id", "price", "compare_at_price",
            "sizes", "stock", "in_stock", "is_digital", "digital_file", "image", "gallery_images",
            "tag", "rating", "is_active", "created_at", "updated_at",
        ]
