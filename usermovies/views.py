import requests
import os
import json

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from requests.auth import HTTPBasicAuth
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.views import APIView
from django.db.models import Count

from .models import User, Collection, Movie
from .serializers import UserSerializer, CollectionSerializer, MovieSerializer, CollectionListSerializer


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


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def movies_list(request):
    if request.method == 'GET':
        data = requests_retry('https://demo.credy.in/api/v1/maya/movies/')
        return Response(data.json())


def requests_retry(url):
    username = "iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0"
    password = "Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1"
    data = requests.get(url, auth=HTTPBasicAuth(username, password))

    if data.status_code == 200:
        return data
    return requests_retry(url)  # Retry Request Recursively


# class CollectionCreateApiView(CreateAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer
#     authentication_classes = (JWTAuthentication, )
#     permission_classes = (IsAuthenticated, )

# def perform_create(self, serializer):
#     serializer.save()

# def create(self, request, *args, **kwargs):
#     response = super().create(request, *args, **kwargs)
#     return Response({
#         'collection_uuid': response.data['uuid']
#     })

class CollectionCreateApiView(APIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        collections = Collection.objects.filter(user=user)
        collection_list = CollectionListSerializer(collections, many=True).data
        movies = Movie.objects.filter(collection__user=user).values('genres')
        genres = [movie['genres'] for movie in movies]
        top3_genres = []

        for i in genres:
            if len(top3_genres) != 3:
                if genres.count(i) > 1:
                    top3_genres.append(i)
                    genres.remove(i)
        if len(top3_genres) != 3:
            for gen in genres:
                if gen not in top3_genres:
                    top3_genres.append(gen)

        response = {
            "is_success": True,
            "data": {
                "collection": collection_list,
                "favourite_genres": top3_genres,
            }
        }

        return Response(response)

    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            collection = Collection.objects.create(title=validated_data['title'],
                                                   description=validated_data['description'],
                                                   user=request.user)
            movie_list = []
            for data in validated_data['movies']:
                movie_list.append(
                    Movie(uuid=data['uuid'], title=data['title'], description=data['description'],
                          genres=data['genres'], collection=collection)
                )
            Movie.objects.bulk_create(movie_list)

            response = {
                'collection_uuid': collection.uuid
            }

            return Response(response)
