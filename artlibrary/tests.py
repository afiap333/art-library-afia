from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.

User=get_user_model()

class LibrarianAuthentication(TestCase):
    def setUp(self):
        self.client=Client()
        self.user=User.objects.create_user(username="test",password="password", email="librarian@gmail.com",user_role="librarian")
    def test_librarian_access(self):
        self.client.force_login(self.user)
        response=self.client.get(reverse("redirect-login"))
        self.assertRedirects(response,reverse("librarian_page"))
class AnonymousUserRedirect(TestCase):
    def setUp(self):
        self.client=Client()
        self.user=User.objects.create_user(username="test",password="password", email="librarian@gmail.com",user_role="anonymous")
    def test_anonymous_access(self):
        response = self.client.get(reverse("anonymous_page"))
        self.assertEqual(response.status_code, 200) 
class PatronRedirect(TestCase):
    def setUp(self):
        self.client=Client()
        self.user=User.objects.create_user(username="test",password="password", email="patron@gmail.com",user_role="patron")
    def test_patron_access(self):
        self.client.force_login(self.user)
        response=self.client.get(reverse("redirect-login"))
        self.assertRedirects(response,reverse("patron_page")) 
class defaultPatron(TestCase):
    def setUp(self):
        self.client=Client()
        self.user=User.objects.create_user(username="test",password="password", email="newpatron@gmail.com")
    def test_patron_access(self):
        self.client.force_login(self.user)
        response=self.client.get(reverse("redirect-login"))
        self.assertRedirects(response,reverse("patron_page")) 