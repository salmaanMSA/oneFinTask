import factory

from faker import Faker
from usermovies.models import User, Collection, Movie

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.name()
    password = fake.text()


class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    title = fake.name() + " Movie Collections"
    description = fake.text()
    user = factory.SubFactory(UserFactory)


class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    uuid = 'hdf4f8w5_dujwbe5e4_dfnwb524'
    title = fake.text()
    description = fake.text()
    genres = fake.text()
    collection = factory.SubFactory(CollectionFactory)