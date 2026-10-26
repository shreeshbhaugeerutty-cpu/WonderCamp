from django.http import Http404
from django.shortcuts import render


RVS = {
    1: {"title": "Class A Motorhomes RV", "subtitle": "High luxury RV", "static_fallback": "images/image 1.png"},
    2: {"title": "Class B Motorhomes RV", "subtitle": "Medium luxury RV", "static_fallback": "images/image 2.png"},
    3: {"title": "Class C Motorhomes RV", "subtitle": "Medium luxury RV", "static_fallback": "images/image 3.png"},
}

def camping_vans(request):
    return render(request, 'RV/rvexplorer.html')


def rv_details(request, rv_id):
    rv = RVS.get(rv_id)
    if rv is None:
        raise Http404("RV not found")
    return render(request, 'RV/rvdetails.html', {"rv": rv})
