from django.urls import path

from . import views

urlpatterns = [
    path('', views.menupanel, name='menupanel'),
    path('newgreenhouse/', views.new_greenhouse, name='newgreenhouse'),
    path('addnewgreenhouse/', views.add_new_greenhouse, name='addnewgreenhouse'),

]