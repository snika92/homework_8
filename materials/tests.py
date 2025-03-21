from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from materials.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru')
        self.course = Course.objects.create(title='Python', owner=self.user)
        self.lesson = Lesson.objects.create(title='Django', video='http://django.youtube.com', course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """ Тестирование просмотра одного урока. """

        url = reverse("materials:lesson_retrieve", args=[self.lesson.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), self.lesson.title
        )

    def test_create_lesson(self):
        """ Тестирование создания урока. """

        url = reverse("materials:lesson_create")

        data = {
            'title': 'Create test',
            'video': 'http://create.youtube.com',
            'course': self.course.pk,
            'owner': self.user.pk
        }

        response = self.client.post(url, data=data)
        # print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "video": "http://create.youtube.com",
                "title": "Create test",
                "description": None,
                "image": None,
                "course": 1,
                "owner": 1
            }
        )

        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        """ Тестирование обновления урока. """

        url = reverse("materials:lesson_update", args=[self.lesson.pk])
        data = {
            'title': 'Update test',
            'video': 'http://update.youtube.com'
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), 'Update test'
        )

    def test_lesson_delete(self):
        """ Тестирование удаления урока. """

        url = reverse("materials:lesson_delete", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_list_lessons(self):
        """ Тестирование вывода списка уроков. """

        url = reverse("materials:lessons_list")

        response = self.client.get(url)
        # print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {"count": 1,
             "next": None,
             "previous": None,
             "results": [{
                 "id": self.lesson.pk,
                 "video": self.lesson.video,
                 "title": self.lesson.title,
                 "description": None,
                 "image": None,
                 "course": self.course.pk,
                 "owner": self.user.pk
             }]}
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru')
        self.course = Course.objects.create(title='Python', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        """ Тестирование создания подписки. """

        url = reverse("materials:subscription")

        data = {
            'course': self.course.pk,
            'user': self.user
        }

        response = self.client.post(url, data=data)
        # print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {"message": "Подписка добавлена"})

    def test_subscription_delete(self):
        """ Тестирование удаления подписки. """
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)
        url = reverse("materials:subscription")
        data = {
            'course': self.course.pk,
            'user': self.user
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {"message": "Подписка удалена"})
