import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Выгружает список ингредиентов в базу данных'

    def handle(self, *args, **options):
        with open('ingredients.csv', encoding='utf-8') as f:
            d = csv.reader(f, delimiter='\n')
            for p in d:
                p = p[0].split(',')
                Ingredient.objects.create(name=p[0], measurement_unit=p[1])
