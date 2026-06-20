from django.urls import path

from .views import UserRetrieveUpdateView

app_name = "users"

urlpatterns = [
    path("profile/", UserRetrieveUpdateView.as_view(), name="profile"),
]
