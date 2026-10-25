

from django.shortcuts import render, get_object_or_404, redirect
from .models import Payment
from .forms import PaymentForm
from bookings.models import Booking


def secure_checkout(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    methods = [
        ('mcb_juice', 'MCB Juice', 'Pay securely using your mobile app'),
        ('credit_card', 'Credit Card', 'Pay via secure gateway')
    ]
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = Payment.objects.create(
                booking=booking,
                amount=booking.amount,
                method=form.cleaned_data['method'],
                mobile=form.cleaned_data['mobile'],
                email=form.cleaned_data['email'],
                country=form.cleaned_data['country'],
                is_successful=True
            )
            return redirect('payment_confirmation', payment_id=payment.id)
    else:
        form = PaymentForm()

    context = {
        'booking': booking,
        'methods': methods,
        'form': form
    }
    return render(request, 'payment.html', context)

def payment_confirmation(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    
    context = {
        'booking': payment.booking,
        'payment': {
            'amount': payment.amount,
            'method_label': payment.get_method_label()
        }
    }
    return render(request, 'payment_confirmation.html', context)