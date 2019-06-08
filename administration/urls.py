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
    path("", views.dashboard, name="dashboard"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("add_employee", views.add_employee, name="add_employee"),
    path("all_employee", views.all_employee, name="all_employee"),
    path("get-zones/<int:id>", views.get_zones, name="get_zones"),
    path("get-executives/<int:id>", views.get_executives, name="get_executives"),
    path("get_employees", views.get_employees, name="get_employees"),
    path("all_users", views.all_users, name="all_users"),
    path("get_users", views.get_users, name="get_users"),
    path("approve_users", views.approve_users, name="approve_users"),
    path("category_import", views.category_import, name="category_import"),
    path("keyword_import", views.keyword_import, name="keyword_import"),
    path("get_sub_category/<int:id>", views.get_sub_category, name="get_sub_category"),
    path("get_keywords/<int:id>", views.get_keywords, name="get_keywords"),
    path("user_login/<int:id>", views.user_login, name="user_login"),
    path("top_keywords", views.top_keywords, name="top_keywords"),
    path("get_hits", views.get_hits, name="get_hits")
]
