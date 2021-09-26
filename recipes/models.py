from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from recipes.validators import value_is_russia, value_must_not_be_null

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name="ingredient name")
    unit = models.CharField(max_length=50, verbose_name="ingredient unit")

    class Meta:
        ordering = ("name",)
        verbose_name = "ingredient"
        verbose_name_plural = "ingredients"

    def __str__(self):
        return f"{self.name}, {self.unit}"


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="tag name")
    color = models.CharField(max_length=50, default="orange",
                             verbose_name="tag color")

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="recipes",
                               verbose_name="recipe author")
    name = models.CharField(max_length=100, unique=True,
                            validators=[value_is_russia],
                            verbose_name="recipe name")
    image = models.ImageField(upload_to="recipes/", blank=True, null=True,
                              verbose_name="recipe image")
    description = models.TextField(verbose_name="recipe description")
    ingredients = models.ManyToManyField(Ingredient,
                                         through="RecipeIngredient",
                                         verbose_name="recipe ingredients")
    tags = models.ManyToManyField(Tag, related_name="recipes",
                                  verbose_name="recipe tags")
    time_cooking = models.PositiveIntegerField(
        validators=[value_must_not_be_null],
        verbose_name="recipe preparation time"
    )
    slug = models.SlugField(unique=True, max_length=75,
                            verbose_name="recipe slug")
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True,
        verbose_name="publication time of the recipe"
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "recipe"
        verbose_name_plural = "recipes"

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name="ingredients_in_recipe",
                               verbose_name="recipe for this ingredient")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name="ingredient_in_recipes",
                                   verbose_name="this ingredient")
    count = models.IntegerField(validators=[MinValueValidator(1)],
                                verbose_name="ingredient amount")

    class Meta:
        verbose_name = "unique ingredient in the recipe"
        verbose_name_plural = "unique ingredients in the recipe"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="favorites",
                             verbose_name="favorite user")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name="favorites",
                               verbose_name="favorite recipe")

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=("user", "recipe"),
            name="unique_favorite_user_recipe"
        )]
        verbose_name = "favorite"
        verbose_name_plural = "favorites"

    def __str__(self):
        return f"Favorite {self.user} {self.recipe}"


class Subscribe(models.Model):
    who_subscribes = models.ForeignKey(User, on_delete=models.CASCADE,
                                       related_name="who_subscribes",
                                       verbose_name="who subscribe")
    who_are_subscribed_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions",
        verbose_name="who are subscribed to"
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=("who_subscribes", "who_are_subscribed_to"),
            name="unique_subscribe"
        )]
        verbose_name = "subscribe"
        verbose_name_plural = "subscribes"

    def __str__(self):
        return (f"{self.who_subscribes} subscribe"
                f" on {self.who_are_subscribed_to}")


class Purchase(models.Model):
    purchaser = models.OneToOneField(User, on_delete=models.CASCADE,
                                     related_name="purchase",
                                     verbose_name="purchaser")
    purchases = models.ManyToManyField(Recipe, related_name="purchases",
                                       verbose_name="purchases")

    class Meta:
        verbose_name = "purchase"
        verbose_name_plural = "purchases"

    def __str__(self):
        return f"Purchase {self.purchaser}"
