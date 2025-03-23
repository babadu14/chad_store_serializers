from rest_framework import mixins, viewsets
from django.contrib.auth import get_user_model
from users.serializers import RegisterSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from users.permissions import IsProfileOwner

User = get_user_model()


class UserListDetailViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin ,viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class RegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]
    
    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=HTTP_204_NO_CONTENT)
