from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login  
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm


from .forms import *
# Create your views here.
def home(request):
    return render (request, 'home.html')

@login_required(login_url='login')
def instagram(request):
    return render(request, 'insta-templates/instagram.html')


# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'registration/registration_form.html', {'form': form})

def signup(request):
    if request.user.is_authenticated:
        return redirect('/instagram')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/instagram')
        else:
            return render(request, 'registration/registration_form.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'registration/registration_form.html', {'form': form})

def signin(request):
    if request.user.is_authenticated:
        return render(request, 'instagram/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/instagram')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'registration/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
