from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/',views.signin , name = 'signin'),
    path('instagram/', views.instagram ,name="instagram"),
    path('',views.home, name='home'),
    path('', views.signout, {"next_page": '/'},name="signout"), 
]