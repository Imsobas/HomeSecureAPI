from django.test import TestCase

# Create your tests here.

from django.contrib import auth

class AuthTestCase(TestCase):
    def setUp(self):
        self.u = User.objects.create_user('test@dom.com','Admin', 'pass')
        self.u.is_staff = True
        self.u.is_superuser = True
        self.u.is_active = True
        self.u.user_role = 'Admin'
        self.u.save()

    def testLogin(self):
        self.client.login(username='test@dom.com', password='pass')