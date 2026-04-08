from rest_framework import serializers
from .models import Category, Product, ProductImage, Review


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'sort', 'is_active', 'children', 'product_count']

    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        return CategorySerializer(children, many=True).data

    def get_product_count(self, obj):
        return obj.products.filter(status='active').count()


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    discount_rate = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'category_name', 'price', 'original_price',
            'stock', 'sales', 'images', 'status', 'is_hot', 'is_recommended',
            'discount_rate', 'created_at'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    discount_rate = serializers.IntegerField(read_only=True)
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'category_name', 'description', 'price',
            'original_price', 'stock', 'sales', 'images', 'specs', 'status',
            'is_hot', 'is_recommended', 'weight', 'discount_rate',
            'review_count', 'average_rating', 'created_at', 'updated_at'
        ]

    def get_review_count(self, obj):
        return obj.reviews.count()

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'description', 'price', 'original_price',
            'stock', 'images', 'specs', 'status', 'is_hot', 'is_recommended', 'weight'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'user_name', 'user_avatar', 'rating', 'content', 'images', 'is_anonymous', 'created_at']
        read_only_fields = ['user', 'created_at']

    def get_user_name(self, obj):
        if obj.is_anonymous:
            return '匿名用户'
        return obj.user.username

    def get_user_avatar(self, obj):
        if obj.is_anonymous:
            return None
        request = self.context.get('request')
        if obj.user.avatar and request:
            return request.build_absolute_uri(obj.user.avatar.url)
        return None

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
