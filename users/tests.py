from django.contrib.auth.models import User
from django.test import TestCase, Client


class TestUserRegister(TestCase):
    def test_register_new(self):
        c = Client()
        response = c.post('/register/',
                          {'username': 'testuser', 'password': 'testpassword', 'confirm_password': 'testpassword',
                           'email': 'a1@example.com'})
        self.assertEqual(response.status_code, 302)
        user_exists = User.objects.filter(username="testuser").all()
        self.assertTrue(user_exists)
        self.assertEqual(len(user_exists), 1)


class TestUserProfile(TestCase):
    def setUp(self):
        new_user = User.objects.create_user(username='testuser', password='testpassword', email='a1@example.com')
        new_user.save()

    def test_user_profile(self):
        c = Client()
        c.login(username='testuser', password='testpassword')
        response = c.post('/user/', {'email': "<EMAIL>", 'first_name': "testuser", 'last_name': "testuser"})
        self.assertEqual(response.status_code, 200)
        saved_user = User.objects.filter(username='testuser').first()
        self.assertEqual(saved_user.first_name, 'testuser')
        self.assertEqual(saved_user.last_name, 'testuser')
        self.assertEqual(saved_user.email, '<EMAIL>')

    def test_user_profile_get(self):
        c = Client()
        c.login(username='testuser', password='testpassword')
        response = c.get('/user/')
        self.assertEqual(response.status_code, 200)
