from django.urls import path
from recipes import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tag/<str:tag>", views.tags_page, name="tag"),
    path("favorite/", views.favorite_page, name="favorite"),
    path("subscribe/", views.subscribe_page, name="subscribe"),
    path("purchase/", views.purchase_page, name="purchase"),
    path("profile/<str:username>/", views.user_page, name="profile"),
    path("recipe/<slug:slug>/", views.recipe_detail, name="recipe"),
    path("create/", views.create_recipe, name="create_recipe"),
    path("recipe/<slug:slug>/update", views.update_recipe, name="update_recipe"),
    path("request/", views.registration_request, name="registration_request"),
    path("author/", views.author_page, name="author_page"),
    path("technology/", views.technology_page, name="technology_page"),
    path("404/", views.page_not_found, name="page_not_found"),
    path("500/", views.server_error, name="server_error"),
]
