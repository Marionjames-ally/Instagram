from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login ,logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *

# Create your views here.
def home(request):
    return render (request, 'home.html')

@login_required(login_url='signup')
def instagram(request):
    return render(request, 'insta-templates/instagram.html')

def signup(request):
    # if request.user.is_authenticated:
    #     return redirect('signup')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            signin(request)
            return redirect('/instagram')
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
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
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
        logout(request)

        return redirect('home')
   
        
@login_required(login_url='login')
def profile(request):
    current_user = request.user
    profile = Profile.objects.all()

    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST,instance=request.user)
        p_form = UpdateUserProfileForm(request.POST, request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            
            return render(request,'registration/profile.html')
    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = UpdateUserProfileForm(instance=request.user.profile)


    context = {
        'u_form':u_form,
        'p_form':p_form,
    }

    return render(request, 'registration/profile.html',locals())

