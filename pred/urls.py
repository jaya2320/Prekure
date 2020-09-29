from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
   path ('register',views.register,name = "register"),# when user wants to signup
   path ('report',views.report,name = "report"),# showing report page
   path('result',views.result, name="result"),# when submit button is clicked
   url(r'find',views.find,name="find"),#when submit to doctor button is clicked
   path('home',views.home,name="home"),#main page where info is entered
   path('signup',views.signup,name="signup"),# when signup is clicked
   path('login',views.login,name="login"),# when login is clicked
   path('searching',views.searching,name="searching"),
   path('enter',views.enter,name="enter"),#starting page showing login
   path('submit',views.submit,name="submit"),
   path('logout',views.logout,name="logout"),
   path('',views.welcome,name="welcome"),
    
]
