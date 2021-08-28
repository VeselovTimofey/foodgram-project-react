from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from recipes.validators import value_is_not_null, value_is_russia

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}, {self.unit}"

    class Meta:
        ordering = ("name",)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50, default="orange")

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="author_recipe")
    name = models.CharField(max_length=100, unique=True,
                            validators=[value_is_russia])
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    description = models.TextField()
    ingredient = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    tag = models.ManyToManyField(Tag, related_name="recipe_tag")
    time_cooking = models.PositiveIntegerField(validators=[value_is_not_null])
    slug = models.SlugField(unique=True, max_length=75)
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-pub_date", )


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name="ingredients_in_recipe")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name="ingredient_in_recipes")
    count = models.IntegerField(validators=[MinValueValidator(1)])


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


class Subscribe(models.Model):
    who_subscribes = models.ForeignKey(User, on_delete=models.CASCADE,
                                       related_name="who_subscribes")
    who_are_subscribed_to = models.ForeignKey(User, on_delete=models.CASCADE,
                                              related_name="subscriptions")

    def __str__(self):
        return (f"{self.who_subscribes} subscribe"
                f" on {self.who_are_subscribed_to}")

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=("who_subscribes", "who_are_subscribed_to"),
            name="unique_subscribe"
        )]


class Purchase(models.Model):
    purchaser = models.OneToOneField(User, on_delete=models.CASCADE,
                                     related_name="user_purchase")
    purchases = models.ManyToManyField(Recipe, related_name="recipe_purchase")

    def __str__(self):
        return f"Purchase {self.purchaser}"
