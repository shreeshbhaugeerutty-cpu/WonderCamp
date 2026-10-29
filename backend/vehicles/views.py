from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

# The price graph and rating label are shared with the campsite pages,
# so both pages look and behave the same way.
from backend.campsites.views import build_price_chart, rating_label

from .data import RVS, RVS_BY_ID, RVS_BY_SLUG
from .forms import RVCommentForm
from .models import RVComment


def camping_vans(request):
    """The Camping Vans (RV) explorer page."""
    rvs = RVS

    # Makes the search bar work: matches the name or the subtitle.
    q = request.GET.get("q", "").strip().lower()
    if q:
        rvs = [
            rv for rv in RVS
            if q in rv["name"].lower() or q in rv["subtitle"].lower()
        ]

    # Add a nicely formatted price, e.g. "Rs 16,500".
    rvs = [{**rv, "price_label": f"Rs {rv['price']:,}"} for rv in rvs]

    return render(request, "RV/rvexplorer.html", {"rvs": rvs})


def rv_detail(request, slug):
    """One page for every RV, filled in from data.py."""
    rv = RVS_BY_SLUG.get(slug)
    if rv is None:
        raise Http404("Camping van not found")

    # ----- Comments: save a new one when the form is submitted -----
    if request.method == "POST":
        form = RVCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.rv_slug = slug
            comment.save()
            # Redirect so refreshing the page doesn't post the comment twice.
            return redirect(reverse("rv_detail", args=[slug]) + "#reviews")
    else:
        initial = {}
        if request.user.is_authenticated:
            initial["name"] = request.user.get_full_name() or request.user.get_username()
        form = RVCommentForm(initial=initial)

    comments = RVComment.objects.filter(rv_slug=slug)

    # ----- Ratings -----
    ratings = [
        {"label": label, "value": f"{value:.1f}", "pct": round(value * 20)}
        for label, value in rv["ratings"].items()
    ]
    overall = round(sum(rv["ratings"].values()) / len(rv["ratings"]), 1)

    reviews = [
        {**review, "pct": round(review["rating"] * 20)}
        for review in rv["reviews"]
    ]

    context = {
        "rv": rv,
        "price": f"Rs {rv['price']:,}",
        "chart": build_price_chart("rv-" + slug, rv["price"]),
        "ratings": ratings,
        "overall": f"{overall:.1f}",
        "overall_pct": round(overall * 20),
        "overall_label": rating_label(overall),
        "reviews": reviews,
        "comments": comments,
        "form": form,
    }
    return render(request, "RV/rvdetails.html", context)


def rv_details_by_id(request, rv_id):
    """Old addresses like /camping-vans/1/ still work: send them to the new page."""
    rv = RVS_BY_ID.get(rv_id)
    if rv is None:
        raise Http404("Camping van not found")
    return redirect("rv_detail", slug=rv["slug"])