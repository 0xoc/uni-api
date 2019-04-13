from django.urls import path
from .views import student_info

urlpatterns = [
    path("student/detail/", student_info.as_view())
]
