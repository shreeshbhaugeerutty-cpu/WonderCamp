from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView

from backend.notifications.models import Notification
from .models import CustomUser
from .forms import ProfileForm

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with this email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'register.html')

        # Create the user
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')

    return render(request, 'register.html')

##Notifications profile management
@login_required
def notifications_profile(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by("-created_at")
    return render(request, "account/notif-profile.html", {"notifications": notifications})


#Password change and reset functions

class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'account/password_change.html'
    success_url = reverse_lazy('profile')
    success_message = 'Your password was changed successfully.'

    def form_valid(self, form):
        print("FORM VALID")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("FORM INVALID:", form.errors)
        return super().form_invalid(form)
#==========================

@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated.')
        return redirect('profile')

    return render(request, 'account/profile.html', {'form': form})


@login_required
@require_POST
def delete_account(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')