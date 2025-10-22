from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import Group
from .forms import SignUpForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

User = get_user_model()


def signUp(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate until email verification
            user.save()
            
            # Note: User will be automatically added to Participant group via signal
            
            messages.success(request, "Account created successfully! Please check your email to activate your account.")
            return render(request, 'accounts/activation_sent.html')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def signout_view(request):
    """User logout view"""
    logout(request)
    return redirect('home')
   


def activate_view(request, user_id, token):
    """Account activation view"""
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, "Invalid activation link.")
        return redirect('login')

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Activate the user
        user.save()
        
        login(request, user)  # Auto-login after activation
        
        messages.success(request, "Your account has been activated successfully! Welcome to Eventify!")
        return redirect('dashboard')
    else:
        messages.error(request, "Activation link is invalid or has expired.")
        return redirect('login')


# @login_required
# def dashboard_redirect(request):
#     """Redirect to appropriate dashboard based on user role"""
#     user = request.user
#     if user.is_superuser or user.groups.filter(name='Admin').exists():
#         return redirect('admin_dashboard')
#     elif user.groups.filter(name='Organizer').exists():
#         return redirect('organizer_dashboard')
#     elif user.groups.filter(name='Participant').exists():
#         return redirect('participant_dashboard')
#     else:
#         # Default to participant dashboard for users without specific role
#         return redirect('participant_dashboard')



