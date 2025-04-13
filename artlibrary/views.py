from django.shortcuts import render,resolve_url,get_object_or_404
from django.http import HttpResponse
from .models import ArtSupply, Message, CustomUser,Collection,CollectionRequest,ArtSupplyRequest
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import AddArtSupplyForm,AddCollectionForm,BorrowForm,ReviewForm
from django.contrib.auth import logout
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter as BaseGoogleOAuth2Adapter
from django.db import models
from django.db.models import Q
from .forms import ProfileForm
from django.contrib import messages
from django.core.mail import send_mail


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
    return redirect('dashboard')

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
    query = request.GET.get('query', '')

    if request.user.user_role == 'anonymous':
        return redirect('artlibrary')
    
    available_items = ArtSupply.objects.all()
    
    print(query)

    if query:
        available_items = ArtSupply.objects.filter(name__icontains=query)
    
    collections = Collection.objects.all()

    context = {
        'available_items': available_items,
        'collections': collections,
        'query': query,
    }
    return render(request, 'artlibrary/librarian.html', context)

@login_required
def librarian_page(request):
    query = request.GET.get('query', '')

    if request.user.user_role == 'anonymous':
        return redirect('artlibrary')
    
    available_items = ArtSupply.objects.all()
    
    print(query)

    if query:
        available_items = ArtSupply.objects.filter(name__icontains=query)
    
    collections = Collection.objects.all()

    context = {
        'available_items': available_items,
        'collections': collections,
        'query': query,
    }
    return render(request, 'artlibrary/librarian.html', context)

@login_required
def dashboard(request):
    if request.user.user_role == 'anonymous':
        return redirect('artlibrary')
    if request.user.user_role == 'patron':
        available_items = ArtSupply.objects.filter(Q(collections_in__isnull=True) | Q(collections_in__is_public=True)).filter(status="available")
    else:
        available_items = ArtSupply.objects.all()

    query = request.GET.get('query', '')
    
    print(query)

    if query:
        available_items = ArtSupply.objects.filter(name__icontains=query)
    
    collections = Collection.objects.all()

    context = {
        'available_items': available_items,
        'collections': collections,
        'query': query,
    }
    return render(request, 'artlibrary/dashboard.html', context)

@login_required
def add_item(request):
    if(request.user.user_role!="librarian"):
        if request.user.user_role=="anonymous":
            return redirect("anonymous_page")
        else:
            return redirect("patron_page")
    collections = Collection.objects.all()
    add_item_form = AddArtSupplyForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if add_item_form.is_valid():
            artSupply = add_item_form.save(commit=False)
            artSupply.added_by = request.user
            artSupply.save()

            selected_public_collections = request.POST.getlist("public_collections")
            for collection_id in selected_public_collections:
                collection = Collection.objects.get(id=collection_id)
                collection.art_supplies.add(artSupply)

            selected_private_collection = request.POST.get("private_collection")
            if selected_private_collection:
                private_collection = Collection.objects.get(id=selected_private_collection)
                private_collection.art_supplies.add(artSupply)

            for collection in Collection.objects.filter(art_supplies=artSupply):
                collection.update_num_items()

            messages.success(request, "Item added successfully!")
            return redirect('librarian_page')

    return render(request, 'artlibrary/add_item.html', {
        'add_item_form': add_item_form,
        'collections': collections
    })

def anonymous_page(request):
    if request.user.is_authenticated:
        user=request.user
    else:
        user=CustomUser(id=0,username="Anonymous",user_role="anonymous")
    available_items = ArtSupply.objects.filter(Q(collections_in__isnull=True) | Q(collections_in__is_public=True)).filter(status="available")
    context = {
        'user':user,
        'available_items': available_items,
    }
    return render(request, 'artlibrary/anonymous.html', context)

@login_required

def patron_page(request):
     query = request.GET.get('query', '')
 
     if query:
         available_items = ArtSupply.objects.filter(name__icontains=query)
     else:
         available_items = ArtSupply.objects.all()
     
     messages = Message.objects.filter(recipient=request.user)
 
     context = {
         'available_items': available_items,
         'messages': messages,
         'query': query,
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
    for collection in Collection.objects.all():
        collection.update_num_items()

    query = request.GET.get('query', '')
    
    print(query)

    if query:
        viewable_collections = viewable_collections.filter(title__icontains=query)

    context = {
        'viewable_collections': viewable_collections,
        'query': query,
    }
    return render(request, 'artlibrary/collections.html', context)
def update_collection(request,id):
    collection = get_object_or_404(Collection, id=id)
    if request.method=='POST':
        form=AddCollectionForm(request.POST,instance=collection,user=request.user)
        if form.is_valid():
            form.save()
            return redirect('collections')
    else:
        form=AddCollectionForm(instance=collection,user=request.user)
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

def edit_item(request, item_id):
    item = get_object_or_404(ArtSupply, id=item_id)
    all_collections = Collection.objects.all()

    if request.method == "POST":
        form = AddArtSupplyForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)

            selected_public_collections = Collection.objects.filter(id__in=request.POST.getlist("public_collections"))
            selected_private_collection = Collection.objects.filter(id=request.POST.get("private_collection")).first()

            if selected_private_collection:
                item.collections.set([selected_private_collection])
            else:
                item.collections.set(selected_public_collections)

            item.save()
            return redirect("some_view")

    else:
        form = AddArtSupplyForm(instance=item)

    return render(request, "edit_item.html", {
        "edit_item_form": form,
        "item": item,
        "collections": all_collections 
    })

def add_collection(request):
    if request.method == "POST":
        print("Form submitted!")
        form = AddCollectionForm(request.POST)
        if form.is_valid():
            print("Form is valid!")

            collection = form.save(commit=False)
            collection.added_by = request.user
            collection.save()

            if not collection.is_public:
                selected_users_ids = request.POST.getlist("private_users")
                print("Selected user IDs:", selected_users_ids)

                selected_users = CustomUser.objects.filter(id__in=selected_users_ids)
                print("Selected Users:", selected_users)

                if selected_users.exists():
                    collection.users.set(selected_users)
                    print("Users successfully added to collection!")
                else:
                    print("No users were selected.")

            return redirect("collections")
        else:
            print("Form errors:", form.errors)
    else:
        form = AddCollectionForm()

    users = CustomUser.objects.all()

    context = {
        'add_collection_form': form,
        'users': users
    }
    return render(request, 'artlibrary/add_collection.html', context)
def item_details(request,id):
    item = get_object_or_404(ArtSupply, id=id)
    collections = Collection.objects.all()
    review_form=ReviewForm()
    reviews=item.ratings.all()
    add_collection_form = AddCollectionForm(user=request.user)
    review_exists = item.ratings.filter(user=request.user).exists()
    print(review_exists)
    if request.method == "POST":
        if "add_to_collection" in request.POST:
            add_collection_form = AddCollectionForm(request.POST, request.FILES, user=request.user)
            if add_collection_form.is_valid():
                collection_ids = request.POST.getlist('collections')  # Get selected collections
                selected_collections = Collection.objects.filter(id__in=collection_ids)
                for collection in selected_collections:
                    collection.items.add(item)  # Add item to each selected collection
                return redirect('item_details', id=id)
    if "submit_review" in request.POST:
        review_form=ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.item=item
            review.user=request.user
            review.save()
            return redirect('item_details',id=id)
    context = {
        'add_collection_form': add_collection_form,
        'review_form':review_form,
        'item': item,
        'collections': collections,
        'reviews':reviews,
        'review_exists':review_exists,
    }
    return render(request, 'artlibrary/item_details.html', context)
def manage_users(request):
    if(request.user.user_role!="librarian"):
        if request.user.user_role=="anonymous":
            return redirect("anonymous_page")
        else:
            return redirect("patron_page")
    usersList= CustomUser.objects.all()
    context={'all_users':usersList}
    return render(request,'artlibrary/manage_users.html',context)
    
def make_librarian(request, id):
    userToUpgrade=get_object_or_404(CustomUser, id=id)
    userToUpgrade.user_role="librarian"
    userToUpgrade.save()
    return redirect("manage_users")
def view_requests(request,id):
    collectionRequests=CollectionRequest.objects.filter(librarian__id=id).filter(is_approved=False)
    itemRequests=ArtSupplyRequest.objects.filter(librarian__id=id).filter(is_approved=False).filter(item__status="available")
    borrowedItems=ArtSupply.objects.filter(added_by=id).filter(status="checked_out")
    context={
        'collectionRequests':collectionRequests,
        'itemRequests':itemRequests,
        'borrowedItems':borrowedItems,
    }
    return render(request,'artlibrary/view_requests.html',context)

def approve_collection_request(request,id):
    collectionRequest=get_object_or_404(CollectionRequest,id=id)
    collectionRequest.collection.users.add(collectionRequest.patron)
    collectionRequest.collection.save()
    collectionRequest.is_approved=True
    collectionRequest.save()
    requestEmail="artlibrary2025@gmail.com"
    recepientEmail=collectionRequest.patron.email
    email_subject="View request approved for"+collectionRequest.collection.title
    email_message="Your request to view the collection "+collectionRequest.collection.title+" has been approved!"
    send_mail(
        email_subject,email_message,requestEmail,[recepientEmail],fail_silently=False,
    )
    return redirect("view_requests",id=request.user.id)

def approve_item_request(request,id):
    supplyRequest=get_object_or_404(ArtSupplyRequest,id=id)
    supplyRequest.item.borrowed_by=supplyRequest.patron
    supplyRequest.item.status="checked_out"
    supplyRequest.is_approved=True
    supplyRequest.item.save()
    supplyRequest.save()
    requestEmail="artlibrary2025@gmail.com"
    recepientEmail=supplyRequest.patron.email
    email_subject="Borrow approved for"+supplyRequest.item.name
    email_message="Your request to borrow the item "+supplyRequest.item.name+" has been approved!"
    send_mail(
        email_subject,email_message,requestEmail,[recepientEmail],fail_silently=False,
    )
    return redirect("view_requests",id=request.user.id)

def request_collection(request,id):
    collectionRequested=get_object_or_404(Collection,id=id)
    existing_request = CollectionRequest.objects.filter(collection=collectionRequested, patron=request.user).first()
    if existing_request:
        return redirect("collections")
    requestedCollection=CollectionRequest.objects.create(collection=collectionRequested,patron=request.user,librarian=collectionRequested.added_by)
    requestEmail="artlibrary2025@gmail.com"
    recepientEmail=requestedCollection.librarian.email
    email_subject="New access request for "+collectionRequested.title
    email_message=requestedCollection.patron.get_full_name()+" requested access to your collection! Go to the Art Supply library to approve now."
    send_mail(
        email_subject,email_message,requestEmail,[recepientEmail],fail_silently=False,
    )
    messages.success(request, "Your request has been submitted successfully!")
    return redirect("collections")

def collection_details(request,id):
    collectionRequested=get_object_or_404(Collection,id=id)
    available_items=ArtSupply.objects.filter(collections_in=collectionRequested).filter(status="available")
    context = {
        'collection':collectionRequested,
        'available_items': available_items,
    }

    query = request.GET.get('query', '')
    
    print(query)

    if query:
        available_items = ArtSupply.objects.filter(name__icontains=query)

    context = {
        'available_items': available_items,
        'collections': collections,
        'query': query,
        'collectionRequested': collectionRequested,
    }
    return render(request, 'artlibrary/collection_details.html', context)

def borrow_item(request,id):
    itemToBorrow=get_object_or_404(ArtSupply,id=id)
    borrow_form=BorrowForm()
    if request.method == 'POST':
        borrow_form=BorrowForm(request.POST)
        if borrow_form.is_valid():
            art_request = borrow_form.save(commit=False)
            art_request.item=itemToBorrow
            art_request.librarian=itemToBorrow.added_by
            art_request.patron=request.user
            art_request.save()
            return redirect('dashboard')
    requestEmail="artlibrary2025@gmail.com"
    recepientEmail=itemToBorrow.added_by.email
    email_subject="New borrow request for "+itemToBorrow.name
    email_message=request.user.get_full_name()+" requested to borrow an item! Go to the Art Supply library to approve now."
    send_mail(
        email_subject,email_message,requestEmail,[recepientEmail],fail_silently=False,
    )
    context={"item":itemToBorrow,"borrow_form":borrow_form}
    return render(request, 'artlibrary/borrow_item.html',context)

def return_item(request,id):
    itemToReturn=get_object_or_404(ArtSupply,id=id)
    itemToReturn.borrowed_by=None
    itemToReturn.status="available"
    itemToReturn.save()
    return redirect("view_requests",id=request.user.id)

def borrowed_items(request):
    available_items = ArtSupply.objects.filter(borrowed_by=request.user)

    query = request.GET.get('query', '')
    
    print(query)

    if query:
        available_items = ArtSupply.objects.filter(name__icontains=query)
    
    collections = Collection.objects.all()

    context = {
        'available_items': available_items,
        'collections': collections,
        'query': query,
    }
    return render(request, 'artlibrary/borrowed_items.html', context)