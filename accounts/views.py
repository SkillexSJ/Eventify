from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.models import Group
from .forms import SignUpForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

User = get_user_model()


def signUp(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # deactivate
            user.save()
                
            messages.success(request, "Account created successfully! Please check your email to activate your account.")
            return render(request, 'accounts/activation_sent.html')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def signout_view(request):
    logout(request)
    return redirect('home')
   


def activate_view(request, user_id, token):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, "Invalid activation link")
        return redirect('login')

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Activate
        user.save()
        
        login(request, user) #login korabo
        
        messages.success(request, "Your account has been activated successfully! Welcome to Eventify!")
        return redirect('dashboard')
    else:
        messages.error(request, "Activation link is invalid or has expired.")
        return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    
    if request.method == 'GET':
        old_messages = messages.get_messages(request)
        old_messages.used = True
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                # Login
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
            
                next_page = request.GET.get('next') or request.POST.get('next', 'dashboard')
                return redirect(next_page)
            else:
                messages.error(request, "Your account is not activated, Please check your email for activation link.")
        else:
            messages.error(request, "Invalid username or password, Please try again.")
    
    return render(request, 'accounts/login.html')



