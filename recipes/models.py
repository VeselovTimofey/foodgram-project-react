from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}, {self.unit}"

    class Meta:
        ordering = ("name",)


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="author_recipe")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="recipes/images/", blank=True, null=True)
    description = models.TextField()
    ingredient = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    tag = models.ManyToManyField("Tag")
    time_cooking = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=75)
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-pub_date", )


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name="recipe")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name="ingredient_in_recipe")
    count = models.PositiveIntegerField()


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user_favorite")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name="favorite_recipe")

    def __str__(self):
        return f"Favorite {self.user} {self.recipe}"

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=("user", "recipe"),
            name="unique_favorite_user_recipe"
        )]
