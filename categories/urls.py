from django.urls import path, include
from .views import  CategoryImageViewSet, CategoryViewSet, CategoryDetailView
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register('categories', CategoryViewSet)

categories_router = routers.NestedDefaultRouter(
    router,
    'categories',
    lookup='category'
)
categories_router.register('images', CategoryImageViewSet)
categories_router.register('detail', CategoryDetailView, basename='category-detail')



urlpatterns = [ 
    path('', include(router.urls)),
    path('', include(categories_router.urls))
]