from django.contrib import admin
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0


class TagInline(admin.TabularInline):
    model = Tag
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, TagInline]


admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Tag)
