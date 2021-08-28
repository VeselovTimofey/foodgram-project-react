from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

apipatterns = [
    path("favorites", views.ApiFavorites.as_view(), name="add_to_favorites"),
    path("favorites/<int:pk>", views.ApiFavorites.as_view(),
         name="remove_from_favorites"),
    path("ingredients", views.GetIngredients.as_view(), name="get_ingredient"),
    path("subscriptions", views.ApiSubscribe.as_view(),
         name="add_to_subscribe"),
    path("subscriptions/<int:pk>", views.ApiSubscribe.as_view(),
         name="remove_from_subscribe"),
    path("purchases", views.ApiPurchase.as_view(), name="add_to_purchase"),
    path("purchases/<int:pk>", views.ApiPurchase.as_view(),
         name="remove_from_purchase"),
]

urlpatterns = format_suffix_patterns(apipatterns, allowed=["json"])
