from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . models import ChatMessage
from django.db.models import Q

# Create your views here.

def homepage(request):
    return render(request, 'chatsystem/home.html')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            current_user = form.save()
            login(request, current_user)
            return redirect('homepage')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {
        'form' : form,
    }

    return render(request, 'chatsystem/user_registration.html', context)

def logout_user(request):
    logout(request)
    return redirect('homepage')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Username or Password is invalid')
    
    return render(request, 'chatsystem/user_login.html')

def all_users(request):
    users = User.objects.filter(is_superuser=False)

    context = {
        'users' : users,
    }

    return render(request, 'chatsystem/all_users.html', context)

@login_required
def private_chat(request, pk):
    other_user = User.objects.get(id=pk)

    all_messages = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(receiver=request.user, sender=other_user)
    ).order_by('timestamp')
    
    context = {
        'other_user' : other_user,
        'all_messages' : all_messages,
    }

    return render(request, 'chatsystem/private_chat.html', context)


def all_groups(request):
    return render(request, 'chatsystem/all_groups.html')