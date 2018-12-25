from django.contrib import admin
from .models import Administrator



# Register your models here.
class UserAdministrator(admin.ModelAdmin):
    list_display = ['id','name','email','phone','password', 'verification_key']


admin.site.register(Administrator, UserAdministrator)