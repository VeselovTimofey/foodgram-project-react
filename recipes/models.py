from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}, {self.unit}"


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="author_recipe")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    description = models.TextField()
    ingredient = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    time_cooking = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=75)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()


class Tag(models.Model):
    name = models.CharField(max_length=50)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.SET_NULL,
                               related_name="tag", null=True)
