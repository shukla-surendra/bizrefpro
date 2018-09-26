from django.contrib import admin
from .models import User, Business,Contact, Media, Cities, Countries, States, Category, Keyword, Website, Executive, BizRefProSearch, Zones

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','phone','address1']


class SearchAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','address','keywords','website','contact','rank']

class BusinessAdmin(admin.ModelAdmin):
    list_display = ['id','business_name','address1','address2','first_name','last_name','email']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug']

class CitiesAdmin(admin.ModelAdmin):
    list_display = ['id','name']

class ZonesAdmin(admin.ModelAdmin):
    list_display = ['id','name']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'email','contact','message','created_at']

class CountriesAdmin(admin.ModelAdmin):
    list_display = ['id','name']

class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','phone','role']
    search_fields = ['role','first_name','last_name']

class KeywordsAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug','category']
    search_fields = []

class MediaAdmin(admin.ModelAdmin):
    list_display = ['id','title','path','media_type']
    search_fields = []

class StatesAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = []

class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'user','category','created_at']
    search_fields = []
    


admin.site.register(User, UserAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Cities, CitiesAdmin)
admin.site.register(Countries, CountriesAdmin)
admin.site.register(States,StatesAdmin)
admin.site.register(Zones, ZonesAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Keyword, KeywordsAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(BizRefProSearch, SearchAdmin)
admin.site.register(Executive, ExecutiveAdmin)






