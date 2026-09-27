from django.shortcuts import render

def campsites(request):
    return render(request, 'campsites/explorer.html')

