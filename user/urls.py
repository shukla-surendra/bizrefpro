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
    path("dashboard", views.dashboard, name="dashboard"),
    path("profile", views.profile, name="profile"),
    path("manage-website", views.manage_website, name="manage_website"),
    path("add-website", views.add_website, name="add_website"),
    path("edit-website/<int:id>", views.edit_website, name="edit_website"),
    path("improve-website", views.improve_website, name="improve_website"),
    path("manage-business", views.manage_business, name="manage_business"),
    path("add-business", views.add_business, name="add_business"),
    path("edit-business/<int:id>", views.edit_business, name="edit_business"),
    path("delete-business/<int:id>", views.delete_business, name="delete_business"),
    path("delete-website/<int:id>", views.delete_website, name="delete_website"),
    path("add-member", views.add_member, name="add_member"),
    path("manage-group", views.manage_group, name="manage_group"),
    path("view-review-detail/<int:id>/<str:review_type>", views.view_review_detail, name="view_review_detail"),
    path("get_business_review/<int:id>/<str:review_type>", views.get_business_review, name="get_business_review"),
    path("get_user_groupes", views.get_user_groupes, name="get_user_groupes"),
    path("detach_user", views.detach_user, name="detach_user"),
    path("get_envitations", views.get_envitations, name="get_envitations"),
    path("download_verification_file/<int:id>", views.download_verification_file, name="download_verification_file"),
    path("verify_site/<int:id>", views.verify_site, name="verify_site"),
    path("logout", views.logout, name="logout")
]
