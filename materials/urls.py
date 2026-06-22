from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (CourseViewSet, LessonListCreateView,
                    LessonRetrieveUpdateDestroyView)

router = DefaultRouter()
router.register("courses", CourseViewSet, basename="courses")

app_name = "materials"

urlpatterns = [
    path("lessons/", LessonListCreateView.as_view(), name="lesson_list_create"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDestroyView.as_view(),
        name="lesson_detail",
    ),
] + router.urls
