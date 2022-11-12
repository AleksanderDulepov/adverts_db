from django.core.management import BaseCommand, CommandError

from advert.models import Advert
from category.models import Category
from user.models import Location, User
from user.utils import load_universal


class Command(BaseCommand):


    def handle(self, *args, **options):
        # load_universal("./user/data/location.csv", Location)
        # load_universal("./user/data/category.csv", Category)
        # load_universal("./user/data/user.csv", User)
        load_universal("./user/data/ad.csv", Advert)

        # try:
        #     # User.objects.all().delete()
        #     # Advert.objects.all().delete()
        #     # Category.objects.all().delete()
        #     load_universal("./user/data/location.csv", Location)
        #     load_universal("./user/data/category.csv", Category)
        #     load_universal("./user/data/user.csv", User)
        #     load_universal("./user/data/ad.csv", Advert)
        #
        # except:
        #     raise CommandError('load data fail')
