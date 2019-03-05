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
    path("", views.index, name="index"),
    path("login-register", views.login_register, name="login_register"),
    path("register-user", views.register, name="register"),
    path("forgot-password", views.forgot_password, name="forgot_password"),
    path("send-password-reset-link", views.reset_link, name="reset_link"),
    path("contact", views.contact, name="contact"),
    path("about-us", views.about, name="about"),
    path("faq", views.faq, name="faq"),
    path("why-join", views.how_it_work, name="how_it_work"),
    path("refer_friend", views.refer_friend, name="refer_friend"),
    path("csr", views.csr, name="csr"),
	path("why-we", views.why_we, name="why_we"),
    path("pricing", views.pricing, name="pricing"),
    path("news", views.news, name="news"),
    path("career", views.career, name="career"),
    path("privacy-policy", views.privacy, name="privacy"),
    path("terms", views.terms, name="terms"),
    path("franchise", views.franchise, name="franchise"),
    path("career", views.career, name="career"),
    path("registration-success", views.registration_success, name="registration-success"),
    path("search-result", views.search_result, name="search_result"),
    path("send_thumbsup_otp", views.send_thumbsup_otp, name="send_thumbsup_otp"),
    path("thums_up", views.thums_up, name="thums_up"),	
    path("thums_down", views.thums_down, name="thums_down"),
    path("search-result-test", views.search_result_test, name="search_result_test"),
    path("hosting-features.html", views.hosting_features, name="hosting_features"),
    #search url
    path("search", views.search, name="search"),
    path("category/<int:category_id>", views.dispaly_business, name="dispaly_business"),
    path("autocomplete", views.autocomplete, name="autocomplete"),
    path("location_autocomplete", views.location_autocomplete, name="location_autocomplete"),
    path("send_refer_otp", views.send_refer_otp, name="send_refer_otp"),
    path("referabusiness", views.referabusiness, name="referabusiness"),
    path("analytics", views.search_analytics, name="search_analytics"),
    #search auto complete
    #path("hosting-features.html", views.hosting_features, name="hosting_features"),
    #sync search index
    #path("syncSearch", views.syncSearch, name="syncSearch"),
    #delete path
    path("delete_media_file", views.delete_media_file, name="delete_media_file"),
    path("import_csv", views.import_csv, name="import_csv"),
    path("reset-user-password/<str:token>", views.reset_password, name="reset_password"),
    #ssl validation
    path(".well-known/pki-validation/E9C6DDCDBC902E658B38F6767EFECD08.txt", views.ssl_validation, name="ssl_validation"),
    path("bizrefpro-promotions", views.bizrefpro_promotions, name="bizrefpro_promotions"),

]
