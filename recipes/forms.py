from recipes.models import Tag, Recipe, Ingredient
from django import forms


class RecipeForm(forms.ModelForm):
    all_tags = Tag.objects.all()
    all_ingredient = Ingredient.objects.all()
    #tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
     #                                    label="Теги",
      #                                   widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Recipe
        fields = ("name", "time_cooking", "description", "image",)
        labels = {"name": "Название рецепта", "time_cooking": "Время приготовления",
                  "description": "Описание", "image": "Загрузить фото"}
        widgets = {
            "name": forms.TextInput(attrs={"class": "form__input"}),
            "time_cooking": forms.NumberInput(attrs={"class": "form__input"}),
            "description": forms.Textarea(attrs={"rows": "8", "class": "form__textarea"}),
        }
