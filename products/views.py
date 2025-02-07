from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from products.models import Product, Review, Cart, ProductTag, FavoriteProduct
from products.serializers import ProductSerializer, ReviewSerializer, CartSerializer, TagSerializer, FavoriteProductSerializer


@api_view(['GET', 'POST'])
def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response({'id':product.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def product_view(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(obj)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def reviews_view(request):
    if request.method == "GET":
        serializer = ReviewSerializer(Review.objects.all(), many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def cart_view(request):
    if request.method == 'GET':
        cart_products = Cart.objects.all()
        serializer = CartSerializer(cart_products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CartSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product added to cart'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET","POST"])
def product_tag_view(request):
    if request.method == "GET":
        tags = ProductTag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Tag added succesfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET", "POST"])
def favorite_product_view(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        favorite_products = FavoriteProduct.objects.all()
        serializer = FavoriteProductSerializer(favorite_products, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = FavoriteProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product added succesfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)