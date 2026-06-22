from django.urls import path

from .views import UserRetrieveUpdateView

from .views import PaymentListView

app_name = "users"

urlpatterns = [
    path("profile/", UserRetrieveUpdateView.as_view(), name="profile"),
    path('payments/', PaymentListView.as_view(), name='payments'),
]
