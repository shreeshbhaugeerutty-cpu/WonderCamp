from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

BOOKING = {
    "reference": "WR-2026-90725",
    "campsite": "Bois Cheri Forest Camp",
    "amount": 9150,
}

METHODS = [
    ("mcb_juice", "MCB Juice", "Third-party payment app"),
    ("sbm", "SBM Banking", ""),
    ("bank", "Bank Transfer", ""),
    ("wallet", "Mobile Wallet", ""),
]


def payment_view(request):
    ctx = {"booking": BOOKING, "methods": METHODS}
    if request.method == "POST":
        if request.POST.get("mobile") and request.POST.get("email"):
            return redirect("payment_done")  # TODO: redirect to MCB Juice, confirm on callback
        ctx["error"] = True
    return render(request, "payment.html", ctx)


def payment_done(request):
    return render(
        request,
        "payment_confirmation.html",
        {
            "booking": BOOKING,
            "payment": {"method_label": "MCB Juice", "amount": BOOKING["amount"]},
        },
    )