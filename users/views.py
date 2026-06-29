from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .filters import PaymentFilter
from .models import Payment, User
from .serializers import PaymentSerializer, UserRegisterSerializer, UserSerializer
from .services import create_stripe_product, create_stripe_price, create_stripe_session


@extend_schema(tags=["Профиль"])
class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["Платежи"])
class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date"]
    permission_classes = [IsAuthenticated]


@extend_schema(tags=["Пользователи"])
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=["Пользователи"])
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=["Пользователи"])
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=["Пользователи"])
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=["Платежи"])
class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        from materials.models import Course
        course_id = self.request.data.get("paid_course")
        course = Course.objects.get(pk=course_id)
        amount = self.request.data.get("amount")

        product_id = create_stripe_product(course.title)
        price_id = create_stripe_price(product_id, int(amount))
        session_id, session_url = create_stripe_session(price_id)

        serializer.save(
            user=self.request.user,
            payment_method=Payment.TRANSFER,
            session_id=session_id,
            payment_link=session_url,
        )