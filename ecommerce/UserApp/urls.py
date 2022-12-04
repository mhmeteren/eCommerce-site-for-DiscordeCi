from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('AccUpdate/', views.AccUpdate, name='AccUpdate'),
    path('resetTOKEN/', views.resetTOKEN, name='resetTOKEN'),
 
]