from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("practices", views.practices, name="practices"),
    path("practices/<str:id>", views.practices_by_id, name="practices-by-id"),
    path("topics", views.topics, name="topics"),
    path("workshops", views.workshops, name="workshops"),
    path("courses/<str:course_id>/workshops", views.workshops_by_course_id, name="workshops-by-course-id"),
    path("workshops/<str:workshop_id>/practices", views.practices_by_workshop_id, name="practices-by-workshop-id"),
    path("workshops/<str:id>", views.workshops_by_id, name="workshops-by-id"),
    path("validate-email", views.validate_email, name="validate-email"),
    path("courses", views.courses, name="courses"),
    path("courses/<str:id>", views.courses_by_id, name="courses_by_id"),
    path("subjects", views.subjects, name="subjects"),
    path("students", views.students, name="students"),
    path("students/<str:id>", views.students_by_id, name="students_by_id")
]
