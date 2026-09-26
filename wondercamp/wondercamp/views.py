from django.shortcuts import render

def landing(request):
    return render(request, 'landing.html')

def campsites(request):
    return render(request, 'campsites/explorer.html')