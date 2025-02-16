from django.urls import path
from products.views import ProductAPIView, ReviewViewSet, CartViewSet, ProductTagView, FavoriteProductViewSet

urlpatterns = [
    path('products/', ProductAPIView.as_view(), name="products"),
    path('products/<int:pk>', ProductAPIView.as_view(), name='product'),
    path('reviews/', ReviewViewSet.as_view(), name="reviews"),
    path('cart/', CartViewSet.as_view(), name='cart'),
    path('tags/', ProductTagView.as_view(), name='tags'),
    path('favorites/', FavoriteProductViewSet.as_view(), name='favorite-product'),
    #path('favorites/<int:pk>', FavoriteProductViewSet.as_view(), name='favorites' )
]