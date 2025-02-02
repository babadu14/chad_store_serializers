from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from products.models import Product, Review, Cart, ProductTag
from products.serializers import ProductSerializer, ReviewSerializer, CartSerializer, TagSerializer, FavoriteProductSerializer


@api_view(['GET', 'POST'])
def product_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        product_list = []
        
        for product in products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'currency': product.currency,
                'quantity': product.quantity
            }
            product_list.append(product_data)

        return Response({'products': product_list})
    elif request.method == "POST":
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            new_product = Product.objects.create(
                name=data.get('name'),
                description=data.get('description'),
                price=data.get('price'),
                currency=data.get('currency', 'GEL'),  
                quantity = data.get('quantity')
            )
            return Response({'id': new_product.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def review_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        review_list = []
        
        for review in reviews:
            review_data = {
                'id': review.id,
                'product_id': review.product.id,
                'content': review.content,
                'rating': review.rating
            }
            review_list.append(review_data)
        
        return Response({'reviews': review_list})

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            review = serializer.save()
            return Response(
                {'id': review.id, 'message': 'Review created successfully!'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def cart_view(request):
    if request.method == 'GET':
        cart_products = Cart.objects.all()
        cart_products_list = []

        for cart in cart_products:
            for product in cart.products.all():
                cart_product_data = {
                    'id': cart.id,
                    'product_id': product.id,
                    'product_name': product.name,
                    'product_description': product.description,
                    'product_price': product.price,
                    'currency': product.currency,
                }
                cart_products_list.append(cart_product_data)

        return Response({"cart_products": cart_products_list})

    elif request.method == 'POST':
        serializer = CartSerializer(data=request.data)

        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data.get('quantity', 1)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

            if request.user.is_authenticated:
                cart, created = Cart.objects.get_or_create(user=request.user)
            else:
                cart, created = Cart.objects.get_or_create(user=None)  

            cart.products.add(product)

            return Response({'message': 'Product added to cart'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET","POST"])
def product_tag_view(request):
    if request.method == "GET":
        products = Product.objects.all()
        products_tags_list = []
        for product in products:
            product_tags = product.tags.all() 

            for tag in product_tags:
                product_tag_data = {
                    'product_id': product.id, 
                    'tag_id': tag.id,
                    'tag_name': tag.name,
                }
                products_tags_list.append(product_tag_data)

        return Response({"product_tags": products_tags_list})
    elif request.method == "POST":
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data["product_id"]
            tag_name = serializer.validated_data["tag_name"]

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            tag, created = ProductTag.objects.get_or_create(name=tag_name)

            product.tags.add(tag)

            return Response(
                {"message": "Tag added successfully", "tag_id": tag.id, "tag_name": tag.name},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def favorite_product_view(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        favorite_products = request.user.favorite_products.all()
        favorite_products_list = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "currency": product.currency,
            }
            for product in favorite_products
        ]

        return Response({"favorite_products": favorite_products_list})

    elif request.method == "POST":
        serializer = FavoriteProductSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data["product_id"]

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


            request.user.favorite_products.add(product)

            return Response(
                {"message": "Product added to favorites", "product_id": product.id},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)