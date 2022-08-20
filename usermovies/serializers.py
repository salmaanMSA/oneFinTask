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


class CollectionCreateSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ("uuid", "title", "description", "movies")

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

class CollectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ("title", "uuid", "description")


class CollectionRetrieveSerializer(serializers.ModelSerializer):
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
