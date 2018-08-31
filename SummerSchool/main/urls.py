"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from main.views import Login, login_success, Gamer_Dashboard, log_out, Game_Details


urlpatterns = [
    # path('', LandingPageView.as_view(), name='home'),
    path('login', Login.as_view(), name='login'),
    path('gamer_dashboard', Gamer_Dashboard.as_view(), name='gamer_dashboard'),
    path('login_success', login_success, name="login_success"),
    path('logout', log_out, name='logout'),
    path('<pk>_game', Game_Details.as_view(), name='game'),

]
