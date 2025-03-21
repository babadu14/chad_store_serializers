from rest_framework.viewsets import ModelViewSet
from products.models import Product, Review, Cart, ProductTag, FavoriteProduct, ProductImage, CartItem
from products.serializers import ProductSerializer, ReviewSerializer, CartSerializer, TagSerializer, FavoriteProductSerializer, ProductImageSerializer, CartItemSerializer
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   RetrieveModelMixin,
                                   UpdateModelMixin,
                                   DestroyModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from products.pagination import ProductPagination
from products.filters import ProductFilter, ReviewFilter
from django.core.exceptions import PermissionDenied
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework.decorators import action
from products.permissions import IsObjectOwnerReadOnly

class ProductAPIView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerReadOnly]
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    throttle_classes = [UserRateThrottle]


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
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, IsObjectOwnerReadOnly]
    filterset_class = ReviewFilter
    
    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs['product_pk'])    
    

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

    def get_queryset(self):
        return self.queryset.filter(product__id=self.kwargs['product_pk'])
    

class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerReadOnly]

    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)
    
    def perform_destroy(self, instance):
        if instance.cart.user != self.request.user:
            raise PermissionDenied('you do not have permission to delete this item')
        instance.delete()
