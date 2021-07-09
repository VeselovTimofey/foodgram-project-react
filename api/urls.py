from django.urls import path
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

apipatterns = [
    path("favorites", views.ApiFavorites.as_view(), name="add_to_favorites"),
    path("favorites/<int:pk>", views.ApiFavorites.as_view(), name="remove_from_favorites"),
    path("ingredients", views.GetIngredients.as_view(), name="get_ingredient"),
]

urlpatterns = format_suffix_patterns(apipatterns, allowed=["json"])
