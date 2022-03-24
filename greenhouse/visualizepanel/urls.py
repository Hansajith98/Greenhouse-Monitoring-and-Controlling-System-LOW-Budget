from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chart', views.send_dashboard_data, name='dashboard-data'),
]

