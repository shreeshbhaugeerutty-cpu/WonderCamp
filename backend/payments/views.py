from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect

from backend.bookings.models import Booking
from .forms import PaymentForm
from .models import Payment


@login_required(login_url='login')
@transaction.atomic
def secure_checkout(request, booking_id):
    Booking.expire_pending()
    booking = get_object_or_404(
        Booking.objects.select_for_update(), pk=booking_id, customer=request.user,
    )
    payment = Payment.objects.filter(booking=booking, is_successful=True).first()
    if payment:
        return redirect('payment_confirmation', payment_id=payment.pk)
    if booking.status != 'pending':
        messages.error(request, 'This booking is not available for payment.')
        return redirect('bookings:my_bookings')

    form = PaymentForm(request.POST if request.method == 'POST' else None,
                       initial={'email': request.user.email, 'country': 'Mauritius'})
    if request.method == 'POST' and form.is_valid():
        # Demo payment only. A live integration must verify provider success first.
        payment, _ = Payment.objects.update_or_create(
            booking=booking,
            defaults={**form.cleaned_data, 'amount': booking.total_cost, 'is_successful': True},
        )
        booking.amount_paid = payment.amount
        booking.payment_method = payment.get_method_label()
        booking.status = 'completed'
        booking.save(update_fields=['amount_paid', 'payment_method', 'status'])
        return redirect('payment_confirmation', payment_id=payment.pk)

    return render(request, 'payments/payment.html', {
        'booking': booking, 'form': form,
        'methods': [
            ('mcb_juice', 'MCB Juice', 'Demo mobile payment'),
            ('credit_card', 'Credit Card', 'Demo card payment'),
        ],
    })


@login_required(login_url='login')
def payment_confirmation(request, payment_id):
    payment = get_object_or_404(
        Payment.objects.select_related('booking'), pk=payment_id,
        booking__customer=request.user, is_successful=True,
    )
    return render(request, 'payments/payment_confirmation.html', {
        'booking': payment.booking,
        'payment': {'amount': payment.amount, 'method_label': payment.get_method_label()},
    })
