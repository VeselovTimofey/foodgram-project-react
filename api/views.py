from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from recipes.models import Favorite


class ApiFavorites(APIView):
    """ Add and remove a recipe from user`s favorites"""
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
