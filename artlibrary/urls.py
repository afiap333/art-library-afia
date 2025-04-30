from django.urls import path, include
from . import views
from .views import update_profile

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("librarian_dashboard/", views.librarian_page, name='librarian_page'),
    path("dashboard/", views.dashboard, name='dashboard'),
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
    path('<int:id>/approve_collection_request/',views.approve_collection_request,name="approve_collection_request"),
    path('<int:id>/deny_collection_request/',views.deny_collection_request,name="deny_collection_request"),
    path('<int:id>/request_collection/',views.request_collection,name="request_collection"),
    path('<int:id>/collection_details/',views.collection_details,name="collection_details"),
    path('add_collection/',views.add_collection,name="add_collection"),

    path('<int:id>/edit_item/', views.edit_item, name='edit_item'),
    path('<int:id>/delete_item',views.delete_item, name="delete_item"),
    path('add_item/',views.add_item,name="add_item"),
    path('<int:id>/item_details/',views.item_details,name="item_details"),
    path('<int:id>/approve_item_request/',views.approve_item_request,name="approve_item_request"),
    path('<int:id>/deny_item_request/',views.deny_item_request,name="deny_item_request"),
    path('<int:id>/borrow_item/',views.borrow_item,name="borrow_item"),
    path('borrowed_items/', views.borrowed_items, name='borrowed_items'),

    path('manage_users/',views.manage_users,name="manage_users"),
    path('<int:id>/make_librarian/',views.make_librarian,name="make_librarian"),
    path('<int:id>/view_requests/',views.view_requests,name="view_requests"),

    path('<int:id>/mark_as_returned/',views.return_item,name="mark_as_returned"),
    path('reviews/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    #path('items/<int:item_id>/', views.item_details, name='item_details'),  # used in cancel button

    path('<int:id>/anonymous_collection_details/',views.anonymous_collection_details,name="anonymous_collection_details"),
    path('anonymous_collections/', views.anonymous_collections, name='anonymous_collections'),
    path('<int:id>/anonymous_item_details/',views.anonymous_item_details,name="anonymous_item_details"),

]