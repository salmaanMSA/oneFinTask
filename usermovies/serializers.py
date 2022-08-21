from .models import User, Collection, Movie
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
        User Serializer
    """
    class Meta:
        model = User
        fields = ("username", "password")


class MovieSerializer(serializers.ModelSerializer):
    """
        Serializer for Movie model
    """
    class Meta:
        model = Movie
        fields = ("uuid", "title", "description", "genres")


class CollectionCreateSerializer(serializers.ModelSerializer):
    """
        Serializer for creating collection
    """
    movies = MovieSerializer(many=True)  # nested serializer

    class Meta:
        model = Collection
        fields = ("uuid", "title", "description", "movies")


class CollectionListSerializer(serializers.ModelSerializer):
    """
        Serializer for listing collections
    """
    class Meta:
        model = Collection
        fields = ("title", "uuid", "description")


class CollectionRetrieveSerializer(serializers.ModelSerializer):
    """
        Serializer for Collection Retrieve
    """
    movies = serializers.SerializerMethodField()

    def get_movies(self, obj):
        try:
            movie_list = Movie.objects.filter(collection=obj)
            serializer = MovieSerializer(movie_list, many=True)
            return serializer.data

        except Movie.DoesNotExist:
            return ""

    class Meta:
        model = Collection
        fields = ("title", "description", "movies")
