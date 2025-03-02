
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from categories.models import Category, CategoryImage
from .serializers import CategoryDetailSerializer, CategoryImageSerializer, CategorySerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class CategoryListView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']

# class CategoryDetailView(RetrieveModelMixin, GenericViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategoryDetailSerializer

    

class CategoryImageViewSet(ListModelMixin,CreateModelMixin,GenericViewSet):
    queryset = CategoryImage.objects.all()
    serializer_class = CategoryImageSerializer

    def get_queryset(self):
        cateogory_id = self.kwargs['category_pk']
        return self.queryset.filter(category=cateogory_id)
    
