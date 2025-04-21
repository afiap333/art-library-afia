from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import ArtSupply,Collection,CollectionRequest,ArtSupplyRequest,CustomUser

# Create your tests here.

User=get_user_model()

class LibrarianAuthentication(TestCase):
    def setUp(self):
        self.client=Client()
        self.user=User.objects.create_user(username="test",password="password", email="librarian@gmail.com",user_role="librarian")
    def test_librarian_access(self):
        self.client.force_login(self.user)
        response=self.client.get(reverse("redirect-login"))
        self.assertRedirects(response,reverse("dashboard"))
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
        self.user=CustomUser.objects.create_user(username="test",password="password", email="patron@gmail.com",user_role="patron")
    def test_patron_access(self):
        self.client.force_login(self.user)
        response=self.client.get(reverse("redirect-login"))
        self.assertRedirects(response,reverse("dashboard")) 
class defaultPatron(TestCase):
    def setUp(self):
        self.client=Client()
        self.user=CustomUser.objects.create_user(username="test",password="password", email="newpatron@gmail.com")
    def test_patron_access(self):
        self.client.force_login(self.user)
        response=self.client.get(reverse("redirect-login"))
        self.assertRedirects(response,reverse("dashboard")) 
class createSupply(TestCase):
    def setUp(self):
        self.client=Client()
        self.user=CustomUser.objects.create_user(username="test",password="password", email="newpatron@gmail.com",user_role="librarian")
        self.supply=ArtSupply.objects.create(name="Test item",quantity=2,status="available",pickup_location="Charlottesville",item_type='single',added_by=self.user)
    def test_supply_created(self):
        self.client.force_login(self.user)
        self.assertEqual(self.supply.name,"Test item")
class borrowSupply(TestCase):
    def setUp(self):
        self.client=Client()
        self.user=CustomUser.objects.create_user(username="test",password="password", email="newpatron@gmail.com",user_role="librarian")
        self.supply=ArtSupply.objects.create(name="Test item",quantity=2,status="available",pickup_location="Charlottesville",item_type='single',added_by=self.user)
    def test_borrow(self):
        self.client.force_login(self.user)
        self.supply.borrowed_by=self.user
        self.assertEqual(self.supply.borrowed_by,self.user)
class editSupply(TestCase):
    #asked chatgpt about testing with forms
    def setUp(self):
        self.client=Client()
        self.user=CustomUser.objects.create_user(username="test",password="password", email="newpatron@gmail.com",user_role="librarian")
        self.supply=ArtSupply.objects.create(name="Test item",quantity=2,status="available",pickup_location="Charlottesville",item_type='single',added_by=self.user)
    def test_edit(self):
        self.client.force_login(self.user)
        url=reverse('edit_item',args=[self.supply.id])
        updatedInfo = {
        "name": "Edited item",
        "quantity": self.supply.quantity,
        "status": self.supply.status,
        "pickup_location": self.supply.pickup_location,
        "item_type": self.supply.item_type,
        "added_by": self.user.id,
        }
        response=self.client.post(url,updatedInfo)
        self.supply.refresh_from_db()
        self.assertEqual(response.status_code,302)
        self.assertEqual(self.supply.name,"Edited item")
class createCollection(TestCase):
    def setUp(self):
        self.client=Client()
        self.user=User.objects.create_user(username="test",password="password", email="newpatron@gmail.com",user_role="librarian")
    def test_collection_created(self):
        self.client.force_login(self.user)
        url=reverse('add_collection')
        collectionInfo={
            "title":"Test Collection",
            "description":"This is a test",
        }
        response=self.client.post(url,collectionInfo)
        self.assertEqual(response.status_code,302)
class editCollection(TestCase):
    def setUp(self):
        self.client=Client()
        self.user=User.objects.create_user(username="test",password="password", email="newpatron@gmail.com",user_role="librarian")
    def test_collection_created(self):
        self.client.force_login(self.user)
        url=reverse('add_collection')
        collectionInfo={
            "title":"Test Collection",
            "description":"This is a test",
        }
        response=self.client.post(url,collectionInfo)
        self.assertEqual(response.status_code,302)
        collection = Collection.objects.get(title="Test Collection")
        editUrl=reverse('edit_collection',args=[collection.id])
        updateCollectionInfo={
            "title":"Edited Collection",
            "description":"This is a test",
            "edit_collection": "1" 
        }
        editResponse=self.client.post(editUrl,updateCollectionInfo)
        self.assertEqual(editResponse.status_code,302)
        collection.refresh_from_db()
        self.assertEqual(collection.title,"Edited Collection")