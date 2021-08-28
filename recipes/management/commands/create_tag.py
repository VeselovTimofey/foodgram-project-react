from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = "Create tag"

    def handle(self, *args, **options):
        tags = [["Завтрак", "orange"], ["Обед", "green"], ["Ужин", "purple"]]
        for tag in tags:
            Tag.objects.get_or_create(name=tag[0], color=tag[1])
            self.stdout.write(self.style.SUCCESS
                              (f"Successfully create tag {tag[0]}"))
