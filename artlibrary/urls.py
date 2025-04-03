from django.urls import path, include
from . import views
from .views import update_profile

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("librarian_dashboard/", views.librarian_page, name='librarian_page'),
    path('', views.index, name='index'),
    path('accounts/', include('allauth.urls')),
    path('redirect-login/', views.login_redirect, name="redirect-login"),
    path('patron/', views.patron_page, name='patron_page'),
    path('anonymous/', views.anonymous_page, name='anonymous_page'),
    path('store-user-role/', views.store_user_role, name='store_user_role'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('', views.logout_view, name='logout'),
    path('collections/', views.collections, name='collections'),
    path('<int:id>/edit_collection/', views.update_collection, name='edit_collection'),
    path('<int:id>/delete_collection/',views.delete_collection, name="delete_collection"),
    path('<int:id>/edit_item/', views.update_item, name='edit_item'),
    path('<int:id>/delete_item',views.delete_item, name="delete_item"),
    path('add_item/',views.add_item,name="add_item"),
    path('<int:id>/item_details/',views.item_details,name="item_details"),
    path('manage_users/',views.manage_users,name="manage_users"),
    path('<int:id>/make_librarian/',views.make_librarian,name="make_librarian"),
]