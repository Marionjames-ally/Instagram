from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login ,logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm


from .forms import *
# Create your views here.
def home(request):
    return render (request, 'home.html')

@login_required(login_url='signup')
def instagram(request):
    return render(request, 'insta-templates/instagram.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('signup')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            signin(request)
            return redirect('/signup')
        else:
            return render(request, 'registration/registration_form.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'registration/registration_form.html', {'form': form})

def signin(request):
    if request.user.is_authenticated:
        return render(request, 'insta-templates/instagram.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password1=password)
        if user is not None:
            login(request, user)
            return redirect('/instagram')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'insta-templates/instagram.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

def signout(request):
    if request.method == "POST":
        logout(request)

        return redirect('home')
   