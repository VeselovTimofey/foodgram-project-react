from io import StringIO

from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import (Favorite, Ingredient, Purchase, Recipe,
                            RecipeIngredient, Subscribe)

from .filters import IngredientFilter
from .serializers import IngredientSerializer


class ApiFavorites(APIView):
    """ Add and remove a recipe from user`s favorites """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        recipe_id = request.data.get("id", None)
        if not recipe_id:
            return Response({"success": False},
                            status=status.HTTP_404_NOT_FOUND)
        Favorite.objects.get_or_create(
            user=request.user,
            recipe_id=recipe_id,
        )
        return Response({"success": True}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        Favorite.objects.filter(recipe_id=pk, user=request.user).delete()
        return Response({"success": True}, status=status.HTTP_200_OK)


class GetIngredients(ListAPIView):
    """ Get ingredient """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    permission_classes = (IsAuthenticated,)


class ApiSubscribe(APIView):
    """ Add and remove subscribe from users """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        who_are_subscribed_to_id = request.data.get("id", None)
        if not who_are_subscribed_to_id:
            return Response({"success": False},
                            status=status.HTTP_404_NOT_FOUND)
        Subscribe.objects.get_or_create(
            who_subscribes=request.user,
            who_are_subscribed_to_id=who_are_subscribed_to_id
        )
        return Response({"success": True}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        Subscribe.objects.filter(
            who_subscribes=request.user,
            who_are_subscribed_to_id=pk,
        ).delete()
        return Response({"success": True}, status=status.HTTP_200_OK)


class ApiPurchase(APIView):
    """ Add and remove purchase from users"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        purchaser = get_object_or_404(Purchase, purchaser=request.user)
        recipes = purchaser.purchases.all().prefetch_related(
            "ingredients_in_recipe"
        )
        ingredients_in_recipe = get_list_or_404(RecipeIngredient,
                                                recipe__in=recipes)
        ingredients = {}
        for ingredient in ingredients_in_recipe:
            name = f"{ingredient.ingredient.name},{ingredient.ingredient.unit}"
            if name in ingredients.keys():
                ingredients[name] += ingredient.count
            else:
                ingredients[name] = ingredient.count
        file = StringIO()
        for ingredient in ingredients:
            index_number = ingredient.find(",")
            name, unit = ingredient[:index_number], ingredient[index_number+1:]
            file.write(f"{name} - {ingredients[ingredient]}{unit}\n")
        response = HttpResponse(file.getvalue(),
                                content_type="application/txt")
        response["Content-Disposition"] = ("attachment;"
                                           " filename=shopping_list.txt")
        file.close()
        return response

    def post(self, request, format=None):
        Purchase.objects.get_or_create(purchaser=request.user)
        purchase = get_object_or_404(Purchase, purchaser=request.user)
        recipe_id = request.data.get("id", None)
        if not recipe_id:
            return Response({"success": False},
                            status=status.HTTP_404_NOT_FOUND)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        purchase.purchases.add(recipe)
        return Response({"success": True}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        purchase = get_object_or_404(Purchase, purchaser=request.user)
        recipe = get_object_or_404(Recipe, id=pk)
        purchase.purchases.remove(recipe)
        return Response({"success": True}, status=status.HTTP_200_OK)
