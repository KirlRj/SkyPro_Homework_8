from celery import shared_task
from django.utils import timezone
from datetime import timedelta


@shared_task
def block_inactive_users():
    from .models import User
    one_month_ago = timezone.now() - timedelta(days=30)
    User.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True,
    ).update(is_active=False)