from rest_framework import serializers
from products.models import Review, Product, Cart


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    currency = serializers.ChoiceField(choices=['GEL', 'USD', 'EUR'])
    quantity = serializers.IntegerField()


class ReviewSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(write_only=True)
    content = serializers.CharField()
    rating = serializers.IntegerField()

    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data['product_id'])
        user = self.context['request'].user

        review = Review.objects.create(
            product=product,
            user=user,
            content=validated_data['content'],
            rating=validated_data['rating'],
        )
        return review
    

class CartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(default=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value


class TagSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(write_only=True)
    tag_name = serializers.CharField()

    def validate(self, data):
        product_id = data.get("product_id")
        tag_name = data.get("tag_name")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product_id": "Invalid product_id. Product does not exist."})

        if product.tags.filter(name=tag_name).exists():
            raise serializers.ValidationError({"tag_name": "This tag already exists for the given product."})

        return data
    
    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value
    
class FavoriteProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if  not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value