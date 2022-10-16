from django.core.management import BaseCommand, CommandError

from crud_func.models import Category, Advert
from crud_func.utils import load_universal


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            Category.objects.all().delete()
            Advert.objects.all().delete()
            load_universal("./crud_func/data/categories.csv", Category)
            load_universal("./crud_func/data/adverts.csv", Advert)
        except:
            raise CommandError('load data fail')
