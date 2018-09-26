"""bizrefpro URL Configuration

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
from django.urls import path, include
from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("lead_detail/<int:id>", views.lead_detail, name="lead_detail"),
    path("setting.html", views.setting, name="setting"),
    path("executive.html", views.executive, name="executive"),
    path("executive/<int:id>", views.executive_list, name="executive_list"),
    path("lead.html", views.lead, name="lead"),
    path("zone-city-manager.html", views.zone_city_manager, name="zone_city_manager"),
    path("lead/<int:id>", views.executive_lead, name="executive_lead"),
    path("get_executive_lead", views.get_executive_lead, name="get_executive_lead"),
    path("logout", views.logout, name="logout"),
    path("get_executive_data", views.get_executive_data, name="get_executive_data"),
    path("get_zonecity_manager", views.get_zonecity_manager, name="get_zonecity_manager")

]
