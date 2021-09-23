from django import forms

from recipes.models import Ingredient, Recipe, Tag


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
