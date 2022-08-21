import pytest

from pytest_factoryboy import register
from tests.factories import UserFactory, CollectionFactory, MovieFactory

register(UserFactory)
register(CollectionFactory)
register(MovieFactory)

@pytest.fixture
def new_user(db, user_factory):
    user = user_factory.create()
    return user

@pytest.fixture
def new_collection(db, collection_factory):
    collection = collection_factory.create()
    return collection

@pytest.fixture
def new_movie(db, movie_factory):
    movie = movie_factory.create()
    return movie