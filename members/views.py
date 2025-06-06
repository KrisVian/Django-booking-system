from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from django.core.mail import send_mail

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')

        else:
            messages.success(request, "There was an error login in. Please try again.")
            return redirect('login')
        

    else:
        return render(request, 'authenticate/login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, "Sign out succesfully")
    return redirect('index')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password = password)
            login(request, user)
            messages.success(request, "Signed in.")
            return redirect('index')
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html', {
        'form':form,
    })