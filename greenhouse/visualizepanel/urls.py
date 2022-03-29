from django.urls import path

from . import views

urlpatterns = [
    path('<str:greenhouse>/', views.index, name='index'),
    path('chart', views.send_dashboard_data, name='dashboard-data'),
    path('controller', views.update_controller, name='dashboard-data'),
]

