from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_course_update_email(course_id):
    from .models import Course, Subscription
    course = Course.objects.get(pk=course_id)
    subscriptions = Subscription.objects.filter(course=course).select_related('user')

    for subscription in subscriptions:
        send_mail(
            subject=f'Обновление курса: {course.title}',
            message=f'Курс "{course.title}" был обновлён. Зайдите и проверьте новые материалы.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscription.user.email],
            fail_silently=False,
        )