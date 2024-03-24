from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    RegisterUserSerializer,
    CustomUserSerializer,
    ChangePasswordSerializer,
    UpdateProfileSerializer,
)
from .models import CustomUser


class RegisterApiView(
    CreateModelMixin,
    GenericViewSet,
):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer


# class CustomTokenObtainPairView(TokenObtainPairView, ModelViewSet):
#     pass


# class CustomTokenObtainPairViewSet(ViewSet):
#     def get_extra_actions(self):
#         return []

#     def create(self, request):
#         return super().create(request)


class GetCurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return CustomUser.objects.get(pk=self.request.user.id)


class UpdateProfileView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer

    def get_object(self):
        return CustomUser.objects.get(pk=self.request.user.id)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
