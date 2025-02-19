from django.shortcuts import render
from django.http import HttpResponse
from .models import ArtSupply, Message
from .forms import AddArtSupplyForm

def index(request):
    return HttpResponse("You're at the library homepage")

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