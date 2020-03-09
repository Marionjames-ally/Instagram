from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login ,logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from .models import *
from .forms import *

# Create your views here.
def home(request):
    return render (request, 'home.html')

@login_required(login_url='signup')
def instagram(request):
    captions = Caption.objects.all()
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = PostForm()
    params = {
        'captions': captions,
        'form': form,
        'users': users,

    }    
    return render(request, 'insta-templates/instagram.html',params)

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
    # if request.user.is_authenticated:
    #     return render(request, 'registration/login.html', {'form': form}')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('instagram')
        else:
            form = AuthenticationForm(request.POST)
            return redirect(request, 'registration/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})


def signout(request):
        logout(request)

        return redirect('login')
   
        
@login_required(login_url='login')
def profile(request, id):
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

@login_required(login_url='login')
def post_comment(request, id):
    image = get_object_or_404(Caption, pk = id)
    is_liked = False
    if image.likes.filter(id=request.user.id).exists():
        is_liked = True
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            savecomment = form.save(commit=False)
            savecomment.post = image
            savecomment.user = request.user.profile
            savecomment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    
    params = {
        'image': image,
        'form': form,
        'is_liked': is_liked,
        'total_likes': image.total_likes()
    }
    return render(request, 'insta-templates/comment.html', params)

@login_required(login_url='login')
def search_profile(request):
    if 'user' in request.GET and request.GET['username']:
        search_term = request.GET.get("username")
        message = f"{search_term}"

        searched_profile = User.search_profile(search_term)
        searched_user = User.objects.filter(username=User)[0]
        return render(request,'insta-templates/search.html')
    else:
         message=''   
    return render(request, 'insta-templates/search.html', {'message':message})
    

@login_required(login_url='login')
def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile')
    user_posts = user_prof.profile.posts.all()
    
    followers = Follow.objects.filter(followed=user_prof.profile)
    follow_status = None
    for follower in followers:
        if request.user.profile == follower.follower:
            follow_status = True
        else:
            follow_status = False
    params = {
        'user_prof': user_prof,
        'user_posts': user_posts,
        'followers': followers,
        'follow_status': follow_status
    }
    print(followers)
    return render(request, 'all-pics/user-profile.html', params)