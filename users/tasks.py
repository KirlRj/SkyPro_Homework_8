from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from users.models import User


@shared_task
def deactivate_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    User.objects.filter(last_login__lt=one_month_ago, is_active=True).update(is_active=False)