from django.urls import path
from recipes import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("profile/<str:username>/", views.ProfileView.as_view(), name="profile"),
    path("recipe/<slug:slug>", views.RecipeDetailView.as_view(), name="recipe"),
]
