from django.urls import path, include
from products.views import ProductAPIView, ReviewViewSet, CartViewSet, ProductTagView, FavoriteProductViewSet, ProductImageViewSet, CartItemViewSet
from rest_framework.routers import SimpleRouter, DefaultRouter

from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', ProductAPIView)
router.register('favorites',FavoriteProductViewSet)
router.register('cart', CartViewSet)
router.register('tags', ProductTagView)



products_router = routers.NestedDefaultRouter(
    router,
    'products',
    lookup='product'
)


router.register('cart_items', CartItemViewSet, basename='cart-items')

products_router.register('images', ProductImageViewSet)
products_router.register('reviews',ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
]

