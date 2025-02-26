from rest_framework.viewsets import ModelViewSet
from products.models import Product, Review, Cart, ProductTag, FavoriteProduct, ProductImage
from products.serializers import ProductSerializer, ReviewSerializer, CartSerializer, TagSerializer, FavoriteProductSerializer, ProductImageSerializer
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   RetrieveModelMixin,
                                   UpdateModelMixin,
                                   DestroyModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet


class ProductAPIView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    

class ReviewViewSet(ListModelMixin, CreateModelMixin,GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs['product_pk'])    

class ProductTagView(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = ProductTag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]



class FavoriteProductViewSet(ModelViewSet):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

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