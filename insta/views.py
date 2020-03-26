from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login ,logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
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
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form})


# def signin(request):
    # if request.user.is_authenticated:
    #     return render(request, 'registration/login.html', {'form': form}')
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password1']
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return redirect('instagram')
    #     else:
    #         form = AuthenticationForm(request.POST)
    #         return redirect(request, 'registration/login.html', {'form': form})
    # else:
    #     form = AuthenticationForm()
    #     return render(request, 'registration/login.html', {'form': form})


def signout(request):
        logout(request)

        return redirect('login')
   
        
@login_required(login_url='login')
def profile(request):
    current_user = request.user
    profile = Profile.objects.all()
    images = request.user.profile.posts.all()

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
        'images':images,
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
    if 'q' in request.GET and request.GET['q']:
        name = request.GET.get("q")

        trial = User.objects.filter(username__icontains=name)[0]
        ids = trial.id
        results = Profile.objects.filter(user_id=ids)

        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'insta-templates/search.html', params)
    else:
        message = ""


    return render(request, 'insta-templates/search.html')
    

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
    return render(request, 'insta-templates/user-profile.html', params)

def unfollow(request,id):
    if request.method == 'GET':
        user_profile2 = Profile.objects.get(pk=id)
        unfollow_d = Follow.objects.filter(follower=request.user.profile, followed=user_profile2)
        unfollow_d.delete()
        return redirect('user_profile', user_profile2.user.username)


def follow(request,id):
    if request.method == 'GET':
        user_profile3 = Profile.objects.get(pk=id)
        follow_s = Follow(follower=request.user.profile, followed=user_profile3)
        follow_s.save()
        return redirect('user_profile', user_profile3.user.username)
