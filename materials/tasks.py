from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail

from materials.models import Course, Subscription


@shared_task
def send_course_update_notification(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course).select_related('user')

    for subscription in subscribers:
        send_mail(
            subject=f"Курс '{course.title}' обновлён",
            message=f"Курс '{course.title}' был недавно обновлён. Зайдите посмотреть.",
            from_email=None,
            recipient_list=[subscription.user.email],
            fail_silently=True,
        )