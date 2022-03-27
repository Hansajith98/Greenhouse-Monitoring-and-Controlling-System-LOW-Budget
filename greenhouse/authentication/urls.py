from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.signIn, name="login"),
    path('postsignIn/', views.postsignIn),
    path('signUp/', views.signUp, name="signup"),
    path('logout/', views.logout, name="log"),
    path('postsignUp/', views.postsignUp),
]
