from django.urls import path, include
from .views import  CategoryImageViewSet, CategoryListView
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register('categories', CategoryListView)

categories_router = routers.NestedDefaultRouter(
    router,
    'categories',
    lookup='category'
)
categories_router.register('images', CategoryImageViewSet)


urlpatterns = [ 
    path('', include(router.urls)),
    path('', include(categories_router.urls))
    # path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    # path('categories/<int:category_id>/images', CategoryImageViewSet.as_view(), name='category-images'),
]