from django.test import TestCase
from django.urls import reverse
from .models import AccessCode, User
from rest_framework import status
from time import sleep
from datetime import datetime

valid_user = {
    'name': 'John',
    'email': 'johndoe@gmail.com',
    'access_code': '12345'
}

invalid_user = {
    'name': None,
    'email': 'johndoe@gmail.com'
}

date = datetime.now().date().strftime('%Y-%m-%d')

valid_mood = {
    'user_id': 1,
    'date': date,
    'emotion': 'Happy'
}

update_mood = {
    'user_id': 1,
    'date': date,
    'emotion': 'Sad'
}

user_url = reverse('user')
mood_url = reverse('mood')

class TestUserView(TestCase):
    def setUp(self):
        AccessCode.objects.create(code='12345')

    def test_create_valid_user(self):
        sleep(1)
        response = self.client.post(user_url, valid_user, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertFalse(AccessCode.objects.filter(code='12345').exists())

    def test_create_user_with_invalid_access_code(self):
        invalid_user_data = valid_user.copy()
        invalid_user_data['access_code'] = 'invalid_code'
        sleep(1)
        response = self.client.post(user_url, invalid_user_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_throttling_after_one_second(self):
        sleep(1)
        response = self.client.post(user_url, valid_user, format='json')
        self.assertEqual(response.status_code, 201)
        response = self.client.post(user_url, valid_user, format='json')
        self.assertEqual(response.status_code, 429)

class TestUserViewGetMethod(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(name='John Doe', email='johndoe@gmail.com')
        self.user2 = User.objects.create(name='Jane Doe', email='janedoe@gmail.com')
        self.user3 = User.objects.create(name='Johnny Appleseed', email='johndoe@gmail.com')  
        AccessCode.objects.create(code='12345')
        
    def test_get_user_with_valid_email(self):
        response = self.client.get(user_url, {'email': 'johndoe@gmail.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  

    def test_get_user_with_no_email(self):
        response = self.client.get(user_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Error: No Email Provided', response.data)

    def test_get_user_with_non_existent_email(self):
        response = self.client.get(user_url, {'email': 'nonexistentemail@gmail.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('No User Found', response.data)

class TestMood(TestCase):
    def setUp(self):
        AccessCode.objects.create(code='12345')
        User.objects.create(name='John Doe', email='johndoe@gmail.com')

    def test_post_mood(self):
        sleep(1)
        response = self.client.post(mood_url, valid_mood)
        self.assertEqual(response.status_code, 201)
    
    def test_update_mood(self):
        sleep(1)
        self.client.post(mood_url, valid_mood)
        sleep(1)
        response = self.client.post(mood_url, update_mood)
        self.assertEqual(response.status_code, 200)

    def test_get_mood(self):
        sleep(1)
        self.client.post(mood_url, valid_mood)
        response = self.client.get(mood_url, {'uid': 1})
        self.assertEqual(response.status_code, 200)
