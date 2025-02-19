from rest_framework import serializers
from products.models import Review, Product, Cart, ProductTag, FavoriteProduct, ProductImage

class ReviewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['product_id', 'content', 'rating']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data.pop('product_id'))
        user = self.context['request'].user
        return Review.objects.create(product=product, user=user, **validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        exclude = ['created_at', 'updated_at']

    def validate_tag_name(self, data):
        product_id = data.get("product_id")
        tag_name = data.get("tag_name")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product_id": "Invalid product_id. Product does not exist."})

        if product.tags.filter(name=tag_name).exists():
            raise serializers.ValidationError({"tag_name": "This tag already exists for the given product."})

        return data
    # ეს მეთოდი ამოწმებს არსებობს თუ არა პროდუქტ და შემდეგ ამოწმებს იმას თუ tag_name არის unique ამ კონკრეტული პროდუქტისთვის
    
    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value
    #ამოწმებს მიცემული product_id შეესაბამება თუ არა რაიმე პროდუქტს
class FavoriteProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = FavoriteProduct
        fields = ['id', 'user', 'product_id', 'product']
        read_only_fields = ['id', 'product']


    def validate_product_id(self, value):
        if  not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value
    #ეს მეთოდი ადასტურებს, რომ product_id არსებობს პროდუქტის Table-ში. 
    # თუ არ არსებობს პროდუქტი მოცემული ID-ით, ის წარმოშობს ValidationError-ს. თუ არსებობს, ის აბრუნებს მნიშვნელობას.

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        user = validated_data.pop('user')

        product = Product.objects.get(id=product_id)
        favorite, created = FavoriteProduct.objects.get_or_create(user=user, product=product)

        if not created:
            raise serializers.ValidationError('This product is already in Favorites')
        return favorite


class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        exclude = ['created_at', 'updated_at',] 
        model = Product


class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    products = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(source = 'products',
                                                     queryset = Product.objects.all(),
                                                     many=True,
                                                     write_only = True)

    class Meta:
        model = Cart
        fields = ['user', 'product_ids', 'products']
    
    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value
#ამოწმებს მიცემული product_id არის თუ არა მონაცემთა ბაზაში

    def create(self, validated_data):
        user = validated_data.pop('user')
        products = validated_data.pop('products')
        cart, _ = Cart.objects.get_or_create(user=user)
        cart.products.add(*products)
        return cart
    

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'product']
        