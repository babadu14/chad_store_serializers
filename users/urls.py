from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserListDetailViewSet, RegisterView

router = DefaultRouter()

router.register('users', UserListDetailViewSet, basename='user')
router.register('register', RegisterView, basename='register')

urlpatterns = [
    path('', include(router.urls)),  
]
