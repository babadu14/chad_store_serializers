from rest_framework import mixins, viewsets
from django.contrib.auth import get_user_model
from users.serializers import RegisterSerializer, ProfileSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from users.permissions import IsProfileOwner
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status, serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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


class PasswordResetRequestViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PasswordResetSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={"uidb64":uid, "token":token})
            )


            send_mail(
                "პაროლის აღდგენა",
                f"დააჭირე ბმულს რომ აღადგინო პაროლი {reset_url}",
                'noreply@example.com',
                [user.email],
                fail_silently=False,
            )

            return Response(
                {"message": "ბმული გაგზავნილია ელფოსტაზე"}, status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetConfirmViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PasswordResetConfirmSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('uidb64', openapi.IN_PATH, description="User ID (base64 encoded)", type=openapi.TYPE_STRING),
            openapi.Parameter('token', openapi.IN_PATH, description="Password reset token", type=openapi.TYPE_STRING),
        ]
    )

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message":"Password succesfully updated"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)