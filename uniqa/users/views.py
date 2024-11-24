from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import CustomUser

def signup_view(request):
    return render(request, 'users/signup.html')

def profile_view(request, pk):
    return render(request, 'users/profile.html')

def profile_edit_view(request):
    return render(request, 'users/profile_edit.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('polls:poll_list')  # Redirect to a specific view
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})

