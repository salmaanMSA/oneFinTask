from django.shortcuts import render
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

class CreateUserApiView(GenericAPIView, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        try:
            user = User.objects.get(username=request.data['username'])
            refresh = RefreshToken.for_user(user)
            response = {
                'status': status.HTTP_201_CREATED,
                'access': str(refresh.access_token)
            }
            return Response(response)
        except ObjectDoesNotExist as exec:
            response = {
                'status': status.HTTP_400_BAD_REQUEST,
                'msg': str(exec)
            }
            return response


