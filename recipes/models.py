from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from recipes.validators import value_is_russia, value_is_not_null

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}, {self.unit}"

    class Meta:
        ordering = ("name",)


class RecipeQuerySet(models.QuerySet):
    def with_is_favorite(self, user_id):
        return self.annotate(is_favorite=models.Exists(
            Favorite.objects.filter(
                user_id=user_id,
                recipe_id=models.OuterRef("pk"),
            ),
        ))


class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50, default="orange")

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="author_recipe")
    name = models.CharField(max_length=100, unique=True, validators=[value_is_russia])
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
