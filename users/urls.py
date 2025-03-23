from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserListDetailViewSet, RegisterView, ProfileViewSet

router = DefaultRouter()

router.register('users', UserListDetailViewSet, basename='user')
router.register('register', RegisterView, basename='register')
router.register('profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),  
]
