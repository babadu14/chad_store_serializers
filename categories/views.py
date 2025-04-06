from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from categories.models import Category, CategoryImage
from categories.serializers import CategoryDetailSerializer, CategoryImageSerializer, CategorySerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from django.core.validators import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser


class CategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name']

class CategoryDetailView(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAuthenticated]

    

class CategoryImageViewSet(mixins.ListModelMixin,mixins.CreateModelMixin,GenericViewSet):
    queryset = CategoryImage.objects.all()
    serializer_class = CategoryImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


    def get_queryset(self):
        cateogory_id = self.kwargs['category_pk']
        return self.queryset.filter(category=cateogory_id)
    
    def create(self, request, *args, **kwargs):
        try:
            super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response ({"error":f"{e}"}, status=status.HTTP_400_BAD_REQUEST)