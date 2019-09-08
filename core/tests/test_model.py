from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """ Test creating a new user with email formate username and PC name """
        email = 'test@pc-name.com'
        password = 'Testpass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Testing normalized email """
        email = 'test@LOND.COM'
        user = get_user_model().objects.create_user(email,'test122')
        self.assertEqual(user.email,email.lower())
    
    def test_new_user_invalid_email(self):
        """ Test create user with no email """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test123')
    
    def test_create_supper_user(self):
        """ Creating Supper User """
        user = get_user_model().objects.create_supperuser(
            'test@supperuser.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

