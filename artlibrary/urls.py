from django.urls import path, include
from . import views

urlpatterns = [
    path("librarian_dashboard/", views.librarian_page, name='librarian_page'),
    path('', views.index, name='index'),
    path('accounts/', include('allauth.urls')),
    path('redirect-login/', views.login_redirect, name="redirect-login"),
    path('patron/', views.patron_page, name='patron_page'),
    path('store-user-role/', views.store_user_role, name='store_user_role'),
]