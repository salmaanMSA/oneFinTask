from .models import User, Collection, Movie
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("uuid", "title", "description", "genres")


class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ("uuid", "title", "description", "movies")


class CollectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ("title", "uuid", "description")
