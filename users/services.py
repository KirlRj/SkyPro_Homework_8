import stripe
from django.conf import settings
from rest_framework.exceptions import APIException

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name: str) -> str:
    try:
        product = stripe.Product.create(name=name)
        return product.id
    except stripe.error.StripeError as e:
        raise APIException(detail=f"Ошибка Stripe при создании продукта: {e.user_message}")


def create_stripe_price(product_id: str, amount: int) -> str:
    try:
        price = stripe.Price.create(
            currency="rub",
            unit_amount=amount * 100,
            product=product_id,
        )
        return price.id
    except stripe.error.StripeError as e:
        raise APIException(detail=f"Ошибка Stripe при создании цены: {e.user_message}")


def create_stripe_session(price_id: str) -> tuple[str, str]:
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
            success_url="http://localhost:8000/users/payments/success/",
            cancel_url="http://localhost:8000/users/payments/cancel/",
        )
        return session.id, session.url
    except stripe.error.StripeError as e:
        raise APIException(detail=f"Ошибка Stripe при создании сессии: {e.user_message}")


def get_stripe_session_status(session_id: str) -> str:
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session.status
    except stripe.error.StripeError as e:
        raise APIException(detail=f"Ошибка Stripe при получении статуса: {e.user_message}")