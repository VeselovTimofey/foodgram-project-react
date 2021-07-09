from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from recipes.models import Favorite, Ingredient
from django.shortcuts import get_object_or_404
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
