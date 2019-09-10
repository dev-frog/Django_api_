from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reversed('user:token')

def create_user(**param):
    return get_user_model().objects.create_user(**param)

class PublicUserApiTests(TestCase):
    """ test user api public """
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ Test creating user with valid """
        payload = {
            'email' : 'test@local.com',
            'password' : ' test122',
            'name' : 'Test name'
        }
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exits(self):
        """ if user all ready exit """
        payload = {'email' : 'test@local.com','password': 'test122'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ Password must be more then 5 char """
        payload = {'email' : 'test@local.com','password' :'pw'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        payload = {'email':'test@local.com','password':'password123'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL,payload)
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credetials(self):
        """ test that token are not create with unvalide creadebtuaks """
        create_user(email='test@local.com',password='test123')
        payload = {'email':'test@local.com','password':'wrong'}
        res = self.client.post(TOKEN_URL,payload)
        self.assertNoIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creat_token_no_user(self):
        payload = {'email':'test@local.com','password':'123'}
        res = self.client.post(TOKEN_URL,payload)
        self.assertNoIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fild(self):
        res = self.client.post(TOKEN_URL,{'email':'one','password': ''})
        self.assertNoIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
