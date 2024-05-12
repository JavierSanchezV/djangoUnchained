from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "prologue/index.html")

def greet(request, name):
    # return HttpResponse(f'Sup {name}?')
    return render(request, "prologue/greet.html", {
        "name": name,
    })