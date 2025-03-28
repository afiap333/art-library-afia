from django.shortcuts import render,resolve_url,get_object_or_404
from django.http import HttpResponse
from .models import ArtSupply, Message, CustomUser,Collection
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import AddArtSupplyForm,AddCollectionForm
from django.contrib.auth import logout
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter as BaseGoogleOAuth2Adapter
from django.db import models
from django.db.models import Q
from .forms import ProfileForm
from django.contrib import messages


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
    if request.user.user_role == 'anonymous':
        return redirect('artlibrary')
    add_item_form = AddArtSupplyForm(request.POST or None, request.FILES or None)
    add_collection_form = AddCollectionForm(request.POST or None, request.FILES or None, user=request.user) 
    if request.method == 'POST':
        if "add_item" in request.POST: 
            add_item_form = AddArtSupplyForm(request.POST, request.FILES)
            if add_item_form.is_valid():
                artSupply = add_item_form.save(commit=False)
                artSupply.added_by = request.user
                artSupply.save()
                return redirect('librarian_page')
        elif "add_collection" in request.POST:
            if add_collection_form.is_valid():
                collection = add_collection_form.save(commit=False)
                collection.added_by = request.user
                collection.save()
                return redirect('librarian_page')
            else:
                print(add_collection_form.errors)
    available_items = ArtSupply.objects.all()
    collections = Collection.objects.all()
    context = {
        'add_item_form': add_item_form,
        'add_collection_form': add_collection_form,
        'available_items': available_items,
        'collections': collections,
    }
    return render(request, 'artlibrary/librarian.html', context)

def add_item(request,id):

    if request.method=='POST':
        form=AddCollectionForm(request.POST,instance=collection)
        if form.is_valid():
            form.save()
            return redirect('collections')
    else:
        form=AddCollectionForm(instance=collection)
    return render(request,'artlibrary/edit_collection.html',{'edit_collection_form':form})


def anonymous_page(request):
    if request.user.is_authenticated:
        user=request.user
    else:
        user=CustomUser(id=0,username="Anonymous",user_role="anonymous")
    available_items = ArtSupply.objects.filter(Q(collection__isnull=True) | Q(collection__is_public=True))
    context = {
        'user':user,
        'available_items': available_items,
    }
    return render(request, 'artlibrary/anonymous.html', context)

@login_required
def patron_page(request):
    available_items = ArtSupply.objects.filter(Q(collection__isnull=True) | Q(collection__is_public=True))
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
    if user_role == "anonymous_user":
        viewable_collections = Collection.objects.filter(is_public=True)
    else:
        viewable_collections = Collection.objects.all()
    add_item_form = AddArtSupplyForm()
    add_collection_form = AddCollectionForm(user=request.user)
    if request.method == "POST":
        if "add_item" in request.POST:
            add_item_form = AddArtSupplyForm(request.POST, request.FILES)
            if add_item_form.is_valid():
                artSupply = add_item_form.save(commit=False)
                artSupply.added_by = request.user
                artSupply.save()
                messages.success(request, "Art supply added successfully!")
                return redirect('librarian_page')
            else:
                print(add_item_form.errors)
                messages.error(request, "Please fix the errors in the form.")
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
    context = {
        'add_collection_form': add_collection_form,
        'viewable_collections': viewable_collections,
        'add_item_form': add_item_form,
    }
    return render(request, 'artlibrary/collections.html', context)
def update_collection(request,id):
    collection = get_object_or_404(Collection, id=id)
    if request.method=='POST':
        form=AddCollectionForm(request.POST,instance=collection)
        if form.is_valid():
            form.save()
            return redirect('collections')
    else:
        form=AddCollectionForm(instance=collection)
    return render(request,'artlibrary/edit_collection.html',{'edit_collection_form':form})

def delete_collection(request,id):
    collection = get_object_or_404(Collection, id=id)
    if request.method=='POST':
        collection.delete()
        return redirect('collections')
    return render(request,'artlibrary/delete_collection.html',{'collection':collection})

def update_item(request,id):
    supply = get_object_or_404(ArtSupply, id=id)
    print(supply)
    if request.method=='POST':
        form=AddArtSupplyForm(request.POST,instance=supply)
        if form.is_valid():
            form.save()
            return redirect('librarian_page')
    else:
        form=AddArtSupplyForm(instance=supply)
    return render(request,'artlibrary/edit_item.html',{'edit_item_form':form})

def delete_item(request,id):
    supply = get_object_or_404(ArtSupply, id=id)
    if request.method=='POST':
        supply.delete()
        return redirect('librarian_page')
    return render(request,'artlibrary/delete_item.html')

