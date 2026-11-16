from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseForbidden
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import User


def register_view(request):
    """
    Handle user registration.
    Validates input, checks for unique username/email, hashes password.
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created successfully for {user.username}! Please log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Handle user login.
    Authenticates with email or username.
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Try to authenticate with email first, then username
            user = authenticate(request, username=username, password=password)
            if user is None and '@' in username:
                # Try with email
                try:
                    user_obj = User.objects.get(email__iexact=username)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                # Redirect to role-based dashboard
                return redirect(user.get_dashboard_url())
            else:
                messages.error(request, 'Invalid email/username or password.')
        else:
            messages.error(request, 'Invalid email/username or password.')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """Handle user logout."""
    username = request.user.username
    logout(request)
    messages.success(request, f'You have been logged out, {username}. See you soon!')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """
    Display user profile.
    Users can only view their own profile.
    """
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})


@login_required
def profile_edit_view(request):
    """
    Handle user profile updates.
    Users can only edit their own profile.
    """
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'accounts/profile_edit.html', {'form': form, 'user': user})


@login_required
def dashboard_view(request):
    """
    Redirect to the appropriate role-based dashboard.
    """
    return redirect(request.user.get_dashboard_url())


@login_required
def admin_dashboard_view(request):
    """
    Admin dashboard - only accessible by admin users.
    """
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('accounts:customer_dashboard')

    # Get statistics for admin dashboard
    total_users = User.objects.count()
    admin_users = User.objects.filter(role=User.Role.ADMIN).count()
    customer_users = User.objects.filter(role=User.Role.CUSTOMER).count()
    recent_users = User.objects.order_by('-created_at')[:5]

    context = {
        'total_users': total_users,
        'admin_users': admin_users,
        'customer_users': customer_users,
        'recent_users': recent_users,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def customer_dashboard_view(request):
    """
    Customer dashboard - only accessible by customer users.
    """
    if not request.user.is_customer():
        messages.error(request, 'You do not have permission to access the customer dashboard.')
        return redirect('accounts:admin_dashboard')

    # Get customer-specific data
    context = {
        'user': request.user,
    }
    return render(request, 'accounts/customer_dashboard.html', context)