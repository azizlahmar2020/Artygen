# accounts/views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import os

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Replace 'home' with your actual home view
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Redirect to profile after successful login
        else:
            messages.error(request, 'Invalid username or password.')  # Show error message
    return render(request, 'accounts/login.html')

@login_required
def profile(request):
    profile_photo = request.user.profile.photo.url if request.user.profile.photo else None
    return render(request, 'accounts/profile.html', {
        'username': request.user.username,
        'profile_photo': profile_photo,
        'PROFILE_PHOTOS_URL': settings.PROFILE_PHOTOS_URL  # Pass the URL to the template
    })

def user_logout(request):
    logout(request)
    return redirect('home')
