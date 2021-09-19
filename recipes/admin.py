from django.contrib import admin

from recipes.models import (Favorite, Ingredient, Purchase, Recipe,
                            RecipeIngredient, Subscribe, Tag)


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
    autocomplete_fields = ("ingredients",)
    inlines = [IngredientInline]


class FavoriteAdmin(admin.ModelAdmin):
    fields = ("user", "recipe",)
    search_fields = ("user", "recipe",)
    list_filter = ("user",)


class TagAdmin(admin.ModelAdmin):
    fields = ("name", "color",)
    list_display = ("name", "color",)
    search_fields = ("name",)


class SubscribeAdmin(admin.ModelAdmin):
    fields = ("who_subscribes", "who_are_subscribed_to",)
    list_filter = ("who_subscribes",)
    search_fields = ("name", "who_are_subscribed_to",)


class PurchaseAdmin(admin.ModelAdmin):
    fields = ("purchaser", "purchases")


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Purchase, PurchaseAdmin)
