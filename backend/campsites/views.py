from django.shortcuts import render, get_object_or_404
from .models import Campsite
 

CAMPSITES = [
    {
        "name": "Mont Choisy Beach Camp",
        "location": "Mont Choisy, Riviere du Rempart, Mauritius",
        "image": "images/mont-choisy.jpg.jpg",
    },
    {
        "name": "Bois Chéri Forest Camp",
        "location": "Bois Chéri, Savanne District, Mauritius",
        "image": "images/bois-cheri.jpg.jpg",
    },
    {
        "name": "Malenga View Point Camping Area",
        "location": "Ripailles, Moka District, Mauritius",
        "image": "images/malenga.jpg.jpg",
    },
    {
        "name": "SAJ Recreation Centre",
        "location": "Riambel, Mauritius",
        "image": "images/saj-recreation.jpg.jpg",
    },
    {
        "name": "Le Morne Mountain Camping",
        "location": "Le Morne, Mauritius",
        "image": "images/le-morne.jpg.jpg",
    },
    {
        "name": "Black River Campsite",
        "location": "Black River Gorges, Mauritius",
        "image": "images/black-river.jpg.jpg",
    },
    {
        "name": "The Dolomites Ranges",
        "location": "Plaines Wilhems",
        "image": "images/dolomites.jpg.jpg",
    },
    {
        "name": "Plaines Vertes Forest",
        "location": "Plaines Vertes, Mauritius",
        "image": "images/plaines-vertes.jpg.jpg",
    },
    {
        "name": "The Lake of Wonder",
        "location": "Mahebourg, Mauritius",
        "image": "images/lake-of-wonder.jpg.jpg",
    },
]
 
 
def explorer(request):
    campsites = CAMPSITES
 
    # Makes the search bar work: matches the name or the location.
    q = request.GET.get("q", "").strip().lower()
    if q:
        campsites = [
            site for site in CAMPSITES
            if q in site["name"].lower() or q in site["location"].lower()
        ]
 
    return render(request, "campsites/explorer.html", {"campsites": campsites})
 
 
def detail(request, pk):
    campsite = get_object_or_404(Campsite, pk=pk)
    return render(request, "campsites/detail.html", {"campsite": campsite})