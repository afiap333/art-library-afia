from django.shortcuts import render,resolve_url
from django.http import HttpResponse
from .models import ArtSupply, Message, CustomUser
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import AddArtSupplyForm
from django.contrib.auth import logout
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

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
@login_required(login_url='/accounts/login/')
def librarian_page(request):
    if request.method == "POST":
        add_item_form = AddArtSupplyForm(request.POST, request.FILES) 
        if add_item_form.is_valid():
            artSupply=add_item_form.save(commit=False)
            artSupply.added_by=request.user
            artSupply.save() 
            return redirect('librarian_page')
    else:
        add_item_form = AddArtSupplyForm()
    available_items = ArtSupply.objects.all()
    messages = Message.objects.filter(recipient=request.user)
    context = {
        'add_item_form': add_item_form,
        'available_items': available_items,
        'messages': messages,
    }
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

    context = {
        'available_items': available_items,
        'messages': messages,
    }

    return render(request, 'artlibrary/patron.html', context)
def profile(request):
    return render(request,'artlibrary/userprofile.html')

def logout_view(request):
    if request.user.is_authenticated:
        request.session.flush()

        social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
        if social_account:
            social_account.socialtoken_set.all().delete()

    logout(request)
    return redirect('index')