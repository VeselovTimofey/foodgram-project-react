import os

from django.core.management.base import BaseCommand
from PIL import Image

from foodgram_project.settings import BASE_DIR
from recipes.models import Recipe

IMAGES_FILE_PATH = os.path.join(BASE_DIR, "recipes images")


class Command(BaseCommand):
    help = "Load images for ingredients"

    def handle(self, *args, **options):
        recipes = Recipe.objects.all()
        for file in os.listdir(IMAGES_FILE_PATH):
            name = file[:file.find(".")]
            if recipes.filter(name=name).exists():
                with Image.open(os.path.join(IMAGES_FILE_PATH, file)) as image:
                    Recipe.objects.filter(name=name).update(image=image)
                    self.stdout.write(self.style.SUCCESS
                                      (f"Successfully update recipe {name}"))
