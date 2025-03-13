from django.shortcuts import render,resolve_url
from django.http import HttpResponse
from .models import ArtSupply, Message, CustomUser
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import AddArtSupplyForm

def index(request):
    return render(request,'artlibrary/index.html')

def store_user_role(request):
    if request.GET.get("anonymous"):  
        request.session['user_role'] = 'anonymous'
        return redirect('anonymous_page')
    role=request.GET.get('role')
    request.session['user_role']=role
    return redirect('account_login')
@login_required
def login_redirect(request):
    role = getattr(request.user, 'user_role', 'patron')
    user = request.user
    print(f"User: {user}, Requested Role: {role}, Actual Role: {getattr(user, 'user_role', 'None')}")
    if role=='librarian':
       return redirect("librarian_page")
    return redirect('patron_page')

def librarian_page(request):
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
    user=request.user
    available_items = ArtSupply.objects.all()
    context = {
        'available_items': available_items,
    }
    return render(request, 'artlibrary/anonymous.html', context)


def patron_page(request):
    available_items = ArtSupply.objects.all()
    messages = Message.objects.filter(recipient=request.user)

    context = {
        'available_items': available_items,
        'messages': messages,
    }

    return render(request, 'artlibrary/patron.html', context)