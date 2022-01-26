from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("validate-email", views.validate_email, name="validate-email")
]