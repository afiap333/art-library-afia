from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("You're at the library homepage")

def librarian_page(request):
    return render(request, 'artlibrary/librarian.html')
