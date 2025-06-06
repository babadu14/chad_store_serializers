from rest_framework.viewsets import ModelViewSet
from products.models import Product, Review, Cart, ProductTag, FavoriteProduct, ProductImage, CartItem
from products.serializers import ProductSerializer, ReviewSerializer, CartSerializer, TagSerializer, FavoriteProductSerializer, ProductImageSerializer, CartItemSerializer
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   RetrieveModelMixin,
                                   UpdateModelMixin,
                                   DestroyModelMixin,)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from products.pagination import ProductPagination
from products.filters import ProductFilter, ReviewFilter
from django.core.exceptions import PermissionDenied
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework.decorators import action
from products.permissions import IsObjectOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from django.core.exceptions import ValidationError

class ProductAPIView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerOrReadOnly]
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        product = self.get_object()
        if product.user != self.request.user:
            raise PermissionDenied("You don't have Permission to update this product")
        serializer.save()

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def my_products(self, request):
        user_products = Product.objects.filter(user=request.user)
        page = self.paginate_queryset(user_products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(user_products, many=True)
        return Response(serializer.data) 


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter
    
    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs['product_pk'])    

    def perform_update(self, serializer):
        review = self.get_object()
        if review.user != self.request.user:
            raise PermissionDenied('you do not have permission to update this review')
        serializer.save()    

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('You do not have permission to delete this review')
        instance.delete()


class ProductTagView(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = ProductTag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]



class FavoriteProductViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin ,DestroyModelMixin, GenericViewSet):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]
    throttle_scope = 'likes'


    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    

class CartViewSet(ListModelMixin,CreateModelMixin,GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
        

    
class ProductImageViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return self.queryset.filter(product__id=self.kwargs['product_pk'])
    
    def create(self, request, *args, **kwargs):
        try:
            super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response ({"error":f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)
    
    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.cart.user != self.request.user:
            raise PermissionDenied('you do not have permission to update this item')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.cart.user != self.request.user:
            raise PermissionDenied('you do not have permission to delete this item')
        instance.delete()
