from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from ratings.models import Rating, Comic


class RatingTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='Test user',
                                 email='testemail@mail',
                                 password='testpassword',
                                 is_active=True)

        User.objects.create_user(username='Test user2',
                                 email='testemail@mail2',
                                 password='testpassword',
                                 is_active=True)

        Comic.objects.create(
            title='Test Comic',
            author='Test Author',
        )
        Rating.objects.create(
            comic_id=Comic.objects.get(),
            user_id=User.objects.get(username='Test user'),
            VALUE=4
        )

    def test_create(self):
        client = APIClient()
        pre_create_rating_count = Rating.objects.count()
        creation_data = {
            'comic_id': Comic.objects.get().id,
            'user_id': User.objects.get(username='Test user2').id,
            'VALUE': 4
        }
        response = client.post('/api/ratings/', creation_data, format='json')
        post_create_rating_count = Rating.objects.count()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post_create_rating_count, pre_create_rating_count + 1)

        new_rating = Rating.objects.get(user_id=User.objects.get(username='Test user2').id)
        self.assertEqual(new_rating.comic_id.id, creation_data['comic_id'])
        self.assertEqual(new_rating.user_id.id, creation_data['user_id'])
        self.assertEqual(new_rating.VALUE, creation_data['VALUE'])

    def test_update(self):
        client = APIClient()
        pre_create_rating_count = Rating.objects.count()
        creation_data = {
            'comic_id': Comic.objects.get().id,
            'user_id': User.objects.get(username='Test user').id,
            'VALUE': 5
        }
        response = client.post('/api/ratings/', creation_data, format='json')
        post_create_rating_count = Rating.objects.count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post_create_rating_count, pre_create_rating_count)

        existing_rating = Rating.objects.get(user_id=User.objects.get(username='Test user'))
        self.assertEqual(existing_rating.VALUE, creation_data['VALUE'])

    def test_comic_rating_update_new(self):
        client = APIClient()
        creation_data = {
            'comic_id': Comic.objects.get().id,
            'user_id': User.objects.get(username='Test user2').id,
            'VALUE': 2
        }
        client.post('/api/ratings/', creation_data, format='json')
        comic = Comic.objects.get()
        self.assertEqual(comic.rating, 3)

    def test_comic_rating_update_existing(self):
        client = APIClient()
        creation_data = {
            'comic_id': Comic.objects.get().id,
            'user_id': User.objects.get(username='Test user').id,
            'VALUE': 2
        }
        client.post('/api/ratings/', creation_data, format='json')
        comic = Comic.objects.get()
        self.assertEqual(comic.rating, 2)


class ComicTestCase(TestCase):
    def setUp(self):
        Comic.objects.create(
            title='Test title',
            author="Test author",
            rating=4
        )
        Comic.objects.create(
            title='Test title2',
            author="Test author",
            rating=3
        )

    def test_get_rating(self):
        client = APIClient()
        comic = Comic.objects.get(title='Test title')
        response = client.get(f'/api/comics/{comic.id}/rating/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], comic.rating)

    def test_get_not_existing_comic(self):
        client = APIClient()
        not_existing_comic_id= 100
        response = client.get(f'/api/comics/{not_existing_comic_id}/rating/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)