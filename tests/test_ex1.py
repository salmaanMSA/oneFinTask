import pytest
from usermovies.models import User


def test_new_user(new_user):
    print("\n User:", new_user.username)
    assert True


def test_collections(new_collection):
    print("\n Collections:", {
        "title": new_collection.title,
        "description": new_collection.description,
        "user": new_collection.user.username
    })
    assert True


def test_movies(new_movie):
    print("\n Movies:", {
        "uuid": new_movie.uuid,
        "title": new_movie.title,
        "description": new_movie.description,
        "collection": new_movie.collection.title
    })
    assert True

