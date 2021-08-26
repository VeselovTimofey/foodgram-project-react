from rest_framework import status, renderers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from recipes.models import Favorite, Ingredient, Subscribe, Purchase, Recipe
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .serializers import IngredientSerializer


class ApiFavorites(APIView):
    """ Add and remove a recipe from user`s favorites """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        Favorite.objects.get_or_create(
            user=request.user,
            recipe_id=request.data["id"],
        )
        return Response({"success": True}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        Favorite.objects.filter(recipe_id=pk, user=request.user).delete()
        return Response({"success": True}, status=status.HTTP_200_OK)


class GetIngredients(ListAPIView):
    """ Get ingredient """
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, format=None):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get("query", None)
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset


class ApiSubscribe(APIView):
    """ Add and remove subscribe from users """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        Subscribe.objects.get_or_create(
            who_subscribes=request.user,
            who_are_subscribed_to_id=request.data["id"],
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
        recipes = Purchase.objects.get(purchaser=request.user).purchases.all()
        purchases = []
        this_ingredient_exist = False
        for recipe in recipes:
            ingredients = recipe.ingredients_in_recipe.all()
            for ingredient in ingredients:
                for element_purchases in purchases:
                    if element_purchases[0] == ingredient.ingredient.name:
                        element_purchases[1] += ingredient.count
                        this_ingredient_exist = True
                        break
                if this_ingredient_exist:
                    this_ingredient_exist = False
                else:
                    element = []
                    element.append(ingredient.ingredient.name)
                    element.append(ingredient.count)
                    element.append(ingredient.ingredient.unit)
                    purchases.append(element)
        with open("media/recipes/purchase.txt", 'w') as file:
            for purchase in purchases:
                file.write(f"{purchase[0]} - {purchase[1]} {purchase[2]}\n")
        with open("media/recipes/purchase.txt", 'r') as file:
            response = HttpResponse(file, content_type='txt')
            response['Content-Disposition'] = 'attachment; filename=media/recipes/purchase.txt'
            return response

    def post(self, request, format=None):
        Purchase.objects.get_or_create(purchaser=request.user)
        purchase = Purchase.objects.get(purchaser=request.user)
        recipe = Recipe.objects.get(id=request.data["id"])
        purchase.purchases.add(recipe)
        return Response({"success": True}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        purchase = Purchase.objects.get(purchaser=request.user,)
        recipe = Recipe.objects.get(id=pk)
        purchase.purchases.remove(recipe)
        return Response({"success": True}, status=status.HTTP_200_OK)
