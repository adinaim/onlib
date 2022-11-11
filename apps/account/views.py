from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from .models import (
    UserProfile
)

from .serializers import (
    UserRegistrationSerializer, 
    PasswordChangeSerializer, 
    RestorePasswordSerializer,
    ResetPasswordSerializer,
    UserProfileCreateSerializer,
    UserProfileListSerializer,
    UserProfileSerializer
    )

from .permissions import IsOwner

User = get_user_model()


class RegistrationView(APIView):
    @swagger_auto_schema(request_body=UserRegistrationSerializer) 
    def post(self, request: Request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):  
            serializer.save()
            return Response(
                'Thanks for registration. Activate your account via link in your email.',
                status=status.HTTP_201_CREATED
                )


class AccountActivationView(APIView):
    def get(self, request, activation_code): 
        user = User.objects.filter(activation_code=activation_code).first()
        if not user:
            return Response(
                'Page not found.' ,
                status=status.HTTP_404_NOT_FOUND
                )
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response(
            'Account activated. You can login now.',
            status=status.HTTP_200_OK
            )


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request:Request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Your password has been changed.',
                status = status.HTTP_200_OK
            )


class RestorePasswordView(APIView):
    def post(self, request: Request):
        serializer = RestorePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response(
                'Code for restoring your password has been sent ot your email.',
                status=status.HTTP_200_OK
            )


class ResetPasswordView(APIView):
    def post(self, request: Request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Your password has been restored.',
                status=status.HTTP_200_OK
            )


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def destroy(self, request: Request):
        username = request.user.username
        User.objects.get(username=username).delete()
        return Response(
            'Your account has been deleted.',
            status=status.HTTP_204_NO_CONTENT
        )


# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)

    # def post(self, request):
    #     try:
    #         refresh_token = request.data["access_token"]
    #         token = RefreshToken(refresh_token)
    #         token.blacklist()
    #         return Response(status=status.HTTP_205_RESET_CONTENT)
    #     except Exception as e:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response(
                'Goodbye, all refresh tokens blacklisted',
                status=status.HTTP_204_NO_CONTENT)
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"})


class ProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def perform_create(self, serializer): # для чего эта функция, чтобы не рописыать юзера в запрроме
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserProfileListSerializer
        elif self.action == 'create':
            return UserProfileCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy']:
            self.permission_classes = [IsOwner, IsAdminUser]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions() 