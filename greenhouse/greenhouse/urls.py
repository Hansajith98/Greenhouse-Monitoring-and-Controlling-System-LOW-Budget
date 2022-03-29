"""greenhouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from visualizepanel import views as visualizeviews
from menupanel import views as menuview
from authentication import views as authenticationview

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('dashboard', views.index, name='index'),path('dashboard/', include('visualizepanel.urls')),
    path('', menuview.menupanel, name="menupanel"),
    path('dashboard/<str:greenhouse>', visualizeviews.index, name='index'),
    path('dashboard/chart/', visualizeviews.send_dashboard_data, name='dashboard-data'),
    path('dashboard/controller/', visualizeviews.update_controller, name='dashboard-data'),
    path('menu/', include('menupanel.urls')),
    # path('menu', menuview.menupanel, name='menupanel'),
    path('authentication/', include('authentication.urls')),
]
