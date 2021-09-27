from django import forms
from django.shortcuts import get_object_or_404

from .models import Ingredient, Recipe, RecipeIngredient, Tag
from .utils import create_slug, get_selected_ingredients, get_selected_tags


class RecipeForm(forms.ModelForm):
    all_ingredients = Ingredient.objects.all()
    all_tags = Tag.objects.all()

    class Meta:
        model = Recipe
        fields = ("name", "time_cooking", "description", "image",)
        labels = {"name": "Название рецепта",
                  "time_cooking": "Время приготовления",
                  "description": "Описание", "image": "Загрузить фото"}
        widgets = {
            "name": forms.TextInput(attrs={"class": "form__input"}),
            "time_cooking": forms.NumberInput(attrs={"class": "form__input"}),
            "description": forms.Textarea(attrs={"rows": "8",
                                                 "class": "form__textarea"}),
        }

    def save(self, request, commit=True):
        recipe = super().save(commit=False)
        recipe.author = request.user
        recipe.slug = create_slug(recipe.name)
        if commit:
            recipe.save()
        tags = get_selected_tags(request)
        recipe.tags.clear()
        for name in tags:
            tag = get_object_or_404(Tag, name=name)
            recipe.tags.add(tag)
        ingredients = get_selected_ingredients(request)
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        for name in ingredients:
            ingredient = get_object_or_404(Ingredient, name=name)
            RecipeIngredient.objects.create(recipe=recipe,
                                            ingredient=ingredient,
                                            count=ingredients[name])
        return recipe
