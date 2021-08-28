import csv
import os

from django.core.management.base import BaseCommand

from foodgram_project.settings import BASE_DIR
from recipes.models import Ingredient

CSV_FILE_PATH = os.path.join(BASE_DIR, "ingredients.csv")


class Command(BaseCommand):
    help = "Load ingredient"

    def handle(self, *args, **options):
        with open(CSV_FILE_PATH, encoding="utf-8") as file:
            reader = csv.reader(file)
            for element in reader:
                name, unit = element
                Ingredient.objects.get_or_create(name=name, unit=unit)
                self.stdout.write(self.style.SUCCESS
                                  (f"Successfully create ingredient {name}"))
