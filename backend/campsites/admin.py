from django.contrib import admin

# Register your models here.
from .models import Campsite

def explorer(request):
    campsites = Campsite.objects.filter(is_available=True)
    return render(request, "campsites/explorer.html", {"campsites": campsites})

def detail(request, pk):
    campsite = get_object_or_404(Campsite, pk=pk)
    return render(request, "campsites/detail.html", {"campsite": campsite})