from django.urls import path
from. import views 

urlpatterns=[
    path("", views.librarian_page, name='librarian_page'),
]