import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name: str) -> str:
    product = stripe.Product.create(name=name)
    return product.id


def create_stripe_price(product_id: str, amount: int) -> str:
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,  # в копейках
        product=product_id,
    )
    return price.id


def create_stripe_session(price_id: str) -> tuple[str, str]:
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
        success_url="http://localhost:8000/users/payments/success/",
        cancel_url="http://localhost:8000/users/payments/cancel/",
    )
    return session.id, session.url

def get_stripe_session_status(session_id: str) -> str:
    session = stripe.checkout.Session.retrieve(session_id)
    return session.status