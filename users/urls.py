from django.urls import path
from users import views

urlpatterns = [
    path("reg/", views.SignUp.as_view(), name='reg')
]
