import factory.fuzzy

from advert.models import Advert
from category.models import Category
from user.models import User




class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model=User

	username=factory.Faker("name")
	password="test_password"
	birth_date="2010-10-10"
	email=factory.Faker("email")
	is_superuser=True

class CategoryFactory(factory.django.DjangoModelFactory):
	class Meta:
		model=Category

	name=factory.Faker("name")
	slug=factory.fuzzy.FuzzyText(length=8)

class AdvertFactory(factory.django.DjangoModelFactory):
	class Meta:
		model=Advert

	name="this_is_test_name"
	author=factory.SubFactory(UserFactory)
	price=1
	description="test_description"
	is_published=False
	category=factory.SubFactory(CategoryFactory)

