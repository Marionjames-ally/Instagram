from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/',views.signin , name = 'signin'),
    path('account/', include('django.contrib.auth.urls'),name="signin"),
    path('instagram/', views.instagram ,name="instagram"),
    path('profile/', views.profile, name="profile"),
    path('',views.home, name='home'),
    path('', views.signout, {"next_page": '/'},name="signout"),
    path('profile/<id>/', views.profile,name = "profile"), 
    path('comment/<id>',views.post_comment,name = 'comment'),
    path('results/', views.search_profile, name = 'results')
]