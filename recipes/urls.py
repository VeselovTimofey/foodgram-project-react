from django.urls import path
from recipes import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index")
]
