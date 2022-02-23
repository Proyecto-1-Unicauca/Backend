from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("practices", views.practices, name="practices"),
    path("practices/<str:id>", views.practices_by_id, name="practices-by-id"),
    path("topics", views.topics, name="topics"),
    path("topics/<str:id>", views.topics_by_id, name="topics-by-id"),
    path("workshops", views.workshops, name="workshops"),
    path("workshops/<str:id>", views.workshops_by_id, name="workshops-by-id"),
    path("validate-email", views.validate_email, name="validate-email"),
    path("courses", views.courses, name="courses"),
    path("courses/<str:id>", views.courses_by_id, name="courses_by_id"),
    path("subjects", views.subjects, name="subjects")
]
