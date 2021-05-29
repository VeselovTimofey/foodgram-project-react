from django.contrib import admin
from recipes.models import Ingredient, Recipe, RecipeIngredient, Favorite, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "unit",)
    search_fields = ("name",)
    list_filter = ("unit",)


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "pub_date")
    search_fields = ("name",)
    list_filter = ("author",)
    autocomplete_fields = ("ingredient",)
    inlines = [IngredientInline]


class FavoriteAdmin(admin.ModelAdmin):
    fields = ("user", "recipe",)
    search_fields = ("user", "recipe",)
    list_filter = ("user",)


class TagAdmin(admin.ModelAdmin):
    fields = ("name",)
    search_fields = ("name",)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Tag, TagAdmin)
