from django.shortcuts import render

def camping_vans(request):
    return render(request, 'RV/rvexplorer.html')
