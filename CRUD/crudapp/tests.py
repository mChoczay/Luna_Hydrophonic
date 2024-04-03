from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from crudapp.models import HydroponicSystem
from crudapp.forms import CreateUserForm, LoginForm, AddSystemForm, UpdateSystemForm

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.system = HydroponicSystem.objects.create(name='Test System', description='Test Description', ph=6.0, water_temperature=20.0, TDS=100.0)

    def test_home(self):
        response = self.client.get(reverse(''))
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_add_system(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)

    def test_update_system(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('update', args=[self.system.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_system(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('view', args=[self.system.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete_system(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('delete', args=[self.system.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after delete

    def test_logout(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout