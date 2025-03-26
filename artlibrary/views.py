from django.shortcuts import render,resolve_url,get_object_or_404
from django.http import HttpResponse
from .models import ArtSupply, Message, CustomUser,Collection
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import AddArtSupplyForm,AddCollectionForm,EditCollectionForm
from django.contrib.auth import logout
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter as BaseGoogleOAuth2Adapter
from django.db import models
from .forms import ProfileForm


def index(request):
    return render(request,'artlibrary/index.html')

def store_user_role(request):
    if request.GET.get("anonymous"):  
        request.session['user_role'] = 'anonymous'
        return redirect('anonymous_page')
    role=request.GET.get('role')
    request.session['user_role']=role
    return redirect('account_login')
@login_required(login_url='/accounts/login/')
def login_redirect(request):
    role = getattr(request.user, 'user_role', 'patron')
    user = request.user
    print(f"User: {user}, Requested Role: {role}, Actual Role: {getattr(user, 'user_role', 'None')}")
    if role=='librarian':
       return redirect("librarian_page")
    return redirect('patron_page')

@login_required
def update_profile(request):
    user = request.user  # Get logged-in user
    
    if request.method == "POST":
        print("POST request received")  # Debugging step
        print("FILES: ", request.FILES)  # See if the file is actually being sent

        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            print("Form is valid. Saving profile picture...")
            form.save()
            print("Profile picture saved!")
            return redirect("profile")  # Redirect to profile page
        else:
            print("Form is NOT valid:", form.errors)  # Debugging output

    else:
        form = ProfileForm(instance=user)

    return render(request, "artlibrary/userprofile.html", {"form": form, "user": user})

@login_required
def librarian_page(request):
    if request.user.user_role=='anonymous':
        return redirect('artlibrary')
    add_item_form = AddArtSupplyForm()
    add_collection_form = AddCollectionForm(request.POST, request.FILES, user=request.user) 
    if "add_item" in request.POST: 
        add_item_form = AddArtSupplyForm(request.POST, request.FILES)
        if add_item_form.is_valid():
            artSupply = add_item_form.save(commit=False)
            artSupply.added_by = request.user
            artSupply.save()
            return redirect('librarian_page')
    if "add_collection" in request.POST:
        add_collection_form = AddCollectionForm(request.POST, request.FILES,user=request.user)
        if add_collection_form.is_valid():
            collection = add_collection_form.save(commit=False)
            collection.added_by = request.user
            collection.save()
            return redirect('librarian_page')
    available_items = ArtSupply.objects.all()
    if request.user.user_role!="anonymous":
        messages = Message.objects.filter(recipient=request.user)
    else: 
        messages=[]
    context = {
        'add_item_form': add_item_form,
        'add_collection_form':add_collection_form,
        'available_items': available_items,
        'messages': messages,
    }
    collections = Collection.objects.all()
    return render(request, 'artlibrary/librarian.html', context)

def anonymous_page(request):
    if request.user.is_authenticated:
        user=request.user
    else:
        user=CustomUser(id=0,username="Anonymous",user_role="anonymous")
    available_items = ArtSupply.objects.all()
    context = {
        'user':user,
        'available_items': available_items,
    }
    return render(request, 'artlibrary/anonymous.html', context)

@login_required
def patron_page(request):
    available_items = ArtSupply.objects.all()
    messages = Message.objects.filter(recipient=request.user)
    add_collection_form = AddCollectionForm(user=request.user)
    if request.method == "POST":
        if "add_collection" in request.POST:
            add_collection_form = AddCollectionForm(request.POST, request.FILES,user=request.user)
            if add_collection_form.is_valid():
                collection = add_collection_form.save(commit=False)
                collection.added_by = request.user
                collection.save()
                return redirect('patron_page')
    context = {
        'add_collection_form': add_collection_form,
        'available_items': available_items,
        'messages': messages,
    }
    return render(request, 'artlibrary/patron.html', context)
def profile(request):
    return render(request,'artlibrary/userprofile.html')

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('index')

class CustomGoogleOAuth2Adapter(BaseGoogleOAuth2Adapter):
    def get_auth_params(self, request, action):
        params = super().get_auth_params(request, action)
        if request.COOKIES.get('force_google_reauth') == 'true':
            params['prompt'] = 'select_account'
            response = request.response
            if response:
                response.delete_cookie('force_google_reauth')
        
        return params
def collections(request):
    user_role = getattr(request.user, 'user_role', None)
    if user_role == "librarian":
        viewable_collections = Collection.objects.all()
    else:
        viewable_collections = Collection.objects.filter(is_public=True)
    add_item_form = AddArtSupplyForm()
    add_collection_form = AddCollectionForm(user=request.user)
    edit_collection_form=EditCollectionForm()
    for collection in viewable_collections:
    if request.method == "POST":
        if "add_item" in request.POST:
            add_item_form = AddArtSupplyForm(request.POST, request.FILES)
            if add_item_form.is_valid():
                art_supply = add_item_form.save(commit=False)
                art_supply.added_by = request.user
                art_supply.save()
                return redirect('librarian_page')
        elif "add_collection" in request.POST:
            add_collection_form = AddCollectionForm(request.POST, request.FILES, user=request.user)
            if add_collection_form.is_valid():
                collection = add_collection_form.save(commit=False)
                collection.added_by = request.user
                collection.save()
                if (user_role == "librarian"):
                    return redirect('librarian_page')
                else:
                    return redirect('patron_dashboard')
        if 'edit_collection' in request.GET:
            collection_id = request.GET['edit_collection']
            collection = get_object_or_404(Collection, id=collection_id)
            if collection.added_by != request.user and user_role != "librarian":
                return redirect('permission_denied')
            edit_collection_form = EditCollectionForm(instance=collection)
            if request.method == 'POST':
                edit_collection_form = EditCollectionForm(request.POST, instance=collection)
                if 'delete_collection' in request.POST and request.POST.get('delete_collection') == 'on':
                    collection.delete()
                    if (user_role == "librarian"):
                        return redirect('librarian_page')
                    else:
                        return redirect('patron_dashboard')
                if edit_collection_form.is_valid():
                    edit_collection_form.save()
                    if (user_role == "librarian"):
                        return redirect('librarian_page')
                    else:
                        return redirect('patron_dashboard')
    context = {
        'add_collection_form': add_collection_form,
        'viewable_collections': viewable_collections,
        'add_item_form': add_item_form,
        'edit_collection_form':edit_collection_form,
    }
    return render(request, 'artlibrary/collections.html', context)
