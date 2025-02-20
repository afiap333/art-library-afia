from django.shortcuts import render,resolve_url
from django.http import HttpResponse
from .models import ArtSupply, Message
from django.shortcuts import redirect
from .forms import AddArtSupplyForm

def index():
    return render(request,'artlibrary/index.html')
def login_redirect(request):
    #user=request.user
    return redirect(resolve_url('librarian_page'))

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