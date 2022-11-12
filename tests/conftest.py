from pytest_factoryboy import register
from tests.factories import AdvertFactory, UserFactory, CategoryFactory

pytest_plugins="tests.fixtures"

register(AdvertFactory)
register(UserFactory)
register(CategoryFactory)