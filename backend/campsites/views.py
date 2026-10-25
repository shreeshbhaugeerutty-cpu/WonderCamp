import random
 
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
 
from .data import CAMPSITES, CAMPSITES_BY_SLUG
from .forms import CommentForm
from .models import Comment
 
 
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
 
 
def rating_label(score):
    if score >= 4.7:
        return "Excellent"
    if score >= 4.3:
        return "Very Good"
    if score >= 3.8:
        return "Good"
    return "Fair"
 
 
def build_price_chart(slug, price, days=30, width=760, height=240):
    """Make a smooth 30-day price graph (as SVG path data) for one campsite.
 
    The numbers are demo values. They're "random", but seeded with the slug,
    so each campsite always gets its own graph and it doesn't change on refresh.
    """
    rng = random.Random(slug)
 
    values = []
    value = price
    for _ in range(days + 1):
        value += rng.uniform(-0.09, 0.09) * price
        value = max(price * 0.75, min(price * 1.25, value))
        values.append(round(value))
 
    low, high = min(values), max(values)
    span = (high - low) or 1
    top, bottom = 12, height - 24  # leave room so the lowest point isn't flat on the axis
 
    points = [
        (i * width / days, bottom - (v - low) / span * (bottom - top))
        for i, v in enumerate(values)
    ]
 
    # Turn the points into a smooth curve (Catmull-Rom spline -> Bezier curves).
    curve = f"M{points[0][0]:.1f},{points[0][1]:.1f}"
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i > 0 else points[i]
        p1, p2 = points[i], points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        curve += (
            f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f}"
            f" {p2[0]:.1f},{p2[1]:.1f}"
        )
 
    area = f"M0,{height} L" + curve[1:] + f" L{width},{height} Z"
 
    ticks = [
        {"label": day, "x": f"{day * width / days:.1f}", "pct": f"{day / days * 100:.2f}"}
        for day in (0, 10, 20, 30)
    ]
 
    return {
        "width": width,
        "height": height,
        "area": area,
        "line": curve,
        "ticks": ticks,
        "low": f"Rs {low:,}",
        "high": f"Rs {high:,}",
    }
 
 
def detail(request, slug):
    site = CAMPSITES_BY_SLUG.get(slug)
    if site is None:
        raise Http404("Campsite not found")
 
    # ----- Comments: save a new one when the form is submitted -----
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.campsite_slug = slug
            comment.save()
            # Redirect so refreshing the page doesn't post the comment twice.
            return redirect(reverse("campsites:detail", args=[slug]) + "#reviews")
    else:
        initial = {}
        if request.user.is_authenticated:
            initial["name"] = request.user.get_full_name() or request.user.get_username()
        form = CommentForm(initial=initial)
 
    comments = Comment.objects.filter(campsite_slug=slug)
 
    # ----- Ratings -----
    ratings = [
        {"label": label, "value": f"{value:.1f}", "pct": round(value * 20)}
        for label, value in site["ratings"].items()
    ]
    overall = round(sum(site["ratings"].values()) / len(site["ratings"]), 1)
 
    reviews = [
        {**review, "pct": round(review["rating"] * 20)}
        for review in site["reviews"]
    ]
 
    context = {
        "site": site,
        "price": f"Rs {site['price']:,}",
        "chart": build_price_chart(slug, site["price"]),
        "ratings": ratings,
        "overall": f"{overall:.1f}",
        "overall_pct": round(overall * 20),
        "overall_label": rating_label(overall),
        "reviews": reviews,
        "comments": comments,
        "form": form,
    }
    return render(request, "campsites/detail.html", context)