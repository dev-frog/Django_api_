from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_supperuser(
            email='admin@local.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'test@local.com',
            password = 'password123',
            name = 'Test user Name'
        )

    def test_user_listed(self):
        """ Test user listing on a page """
        url = reverse('admin:core_user_changelist')
        req = self.client.get(url)
        self.assertContains(req,self.user.name)
        self.assertContains(req,self.user.email)

    def test_user_change_page(self):
        """ Test User eidt Page """
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code,200)

    def test_create_user_page(self):
        """ Test that the create user page work """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code,200)
