from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@test.com", password="pass12345"
        )
        self.other_user = User.objects.create_user(
            email="other@test.com", password="pass12345"
        )
        self.moderator = User.objects.create_user(
            email="mod@test.com", password="pass12345"
        )
        moderator_group = Group.objects.create(name="Модераторы")
        self.moderator.groups.add(moderator_group)

        self.course = Course.objects.create(
            title="Курс", description="Описание", owner=self.owner
        )
        self.lesson = Lesson.objects.create(
            title="Урок",
            description="Описание",
            video_link="https://youtube.com/watch?v=123",
            course=self.course,
            owner=self.owner,
        )

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("materials:lesson_list_create")
        data = {
            "title": "Новый урок",
            "description": "Описание",
            "video_link": "https://youtube.com/watch?v=456",
            "course": self.course.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_invalid_link(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("materials:lesson_list_create")
        data = {
            "title": "Плохой урок",
            "description": "Описание",
            "video_link": "https://vimeo.com/123",
            "course": self.course.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_lesson(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("materials:lesson_detail", args=[self.lesson.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.lesson.title)

    def test_update_lesson_by_owner(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("materials:lesson_detail", args=[self.lesson.id])
        response = self.client.patch(url, {"title": "Обновлённый урок"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson_by_owner(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("materials:lesson_detail", args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lesson_by_moderator_forbidden(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lesson_detail", args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_lesson_by_moderator_forbidden(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lesson_list_create")
        data = {
            "title": "Урок модератора",
            "description": "Описание",
            "video_link": "https://youtube.com/watch?v=789",
            "course": self.course.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_lesson_by_other_user_forbidden(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse("materials:lesson_detail", args=[self.lesson.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_lesson_by_anonymous_unauthorized(self):
        url = reverse("materials:lesson_detail", args=[self.lesson.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="subuser@test.com", password="pass12345"
        )
        self.course = Course.objects.create(
            title="Курс", description="Описание", owner=self.user
        )

    def test_subscribe(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:subscribe")
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_unsubscribe(self):
        self.client.force_authenticate(user=self.user)
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse("materials:subscribe")
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
