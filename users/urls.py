from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import PaymentListView, UserRetrieveUpdateView, UserDeleteView, UserDetailView, UserListView, \
    UserRegisterView

app_name = "users"

urlpatterns = [
    path("profile/", UserRetrieveUpdateView.as_view(), name="profile"),
    path("payments/", PaymentListView.as_view(), name="payments"),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', UserListView.as_view(), name='user_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]
