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
from .serializers import UserSerializer, CollectionCreateSerializer, MovieSerializer, CollectionListSerializer, \
    CollectionRetrieveSerializer
from moviecluster import settings


# Create your views here.

class CreateUserApiView(GenericAPIView, CreateModelMixin):
    """
        User Registration API
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        try:
            # get user
            user = User.objects.get(username=request.data['username'])
            # generate refresh token for user
            refresh = RefreshToken.for_user(user)
            response = {
                'access': str(refresh.access_token)
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            response = {
                'msg': "Error"
            }
            return response


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def movies_list(request):
    """
        Third party api integration
    """
    if request.method == 'GET':
        data = requests_retry('https://demo.credy.in/api/v1/maya/movies/')
        return Response(data.json())


def requests_retry(url):
    """
        Api Retry Mechanism Using Recursion
    """
    # auth credentials
    username = settings.USERNAME
    password = settings.PASSWORD
    data = requests.get(url, auth=HTTPBasicAuth(username, password))

    if data.status_code == 200:
        return data
    return requests_retry(url)  # Retry Request Recursively


class CollectionApiView(APIView):
    """
        CRUD Operation - Collections
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, uuid=None):
        user = request.user
        # get user collections
        if uuid is None:
            collections = Collection.objects.filter(user=user)
            collection_list = CollectionListSerializer(collections, many=True).data
            # query for top3 genres based on movie collections
            movies = Movie.objects.values("genres").annotate(count=Count('id')).filter(collection__user=user).order_by(
                '-count')
            genres = [movie['genres'] for movie in movies]
            top3_genres = []

            for i in genres:
                if len(top3_genres) != 3:
                    if genres.count(i) > 1:
                        top3_genres.append(i)
                        genres.remove(i)
            if len(top3_genres) != 3:
                for gen in genres:
                    if len(top3_genres) != 3:
                        if gen not in top3_genres:
                            top3_genres.append(gen)

            response = {
                "is_success": True,
                "data": {
                    "collection": collection_list,
                    "favourite_genres": top3_genres,
                }
            }

            return Response(response, status=status.HTTP_200_OK)

        else:
            # Retrieve specific collections
            collection = Collection.objects.filter(user=user, uuid=uuid)
            if collection:
                serializer = CollectionRetrieveSerializer(collection, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                response = {
                    "error": "Wrong Collection ID"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # create new collections
        serializer = CollectionCreateSerializer(data=request.data)
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

            return Response(response, status=status.HTTP_201_CREATED)

        else:
            response = {
                "error": serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, uuid):
        try:
            collection = Collection.objects.get(uuid__exact=uuid)
            serializer = CollectionCreateSerializer(collection, data=request.data)
            print(request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                collection.title = validated_data['title']
                collection.description = validated_data['description']
                collection.save()

                for data in validated_data['movies']:
                    try:
                        movie = Movie.objects.get(uuid__exact=data['uuid'], collection=collection)
                        movie.title = data['title']
                        movie.uuid = data['uuid']
                        movie.description = data['description']
                        movie.save()

                    except Movie.DoesNotExist:
                        new_movie = Movie.objects.create(uuid=data['uuid'], title=data['title'],
                                                         description=data['description'], collection=collection)

                response = {
                    "is_Success": True,
                    "Msg": "Collection Updated Successfully"
                }

                return Response(response, status=status.HTTP_200_OK)

            else:
                response = {
                    "error": serializer.errors
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        except Collection.DoesNotExist:
            response = {
                "error": "Invalid Collection UUID"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        try:
            collection = Collection.objects.get(uuid=uuid)
            collection.delete()
            response = {
                "Msg": "Collection Deleted Successfully"
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        except Collection.DoesNotExist:
            response = {
                "Msg": "Invalid Collection UUID"
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)


