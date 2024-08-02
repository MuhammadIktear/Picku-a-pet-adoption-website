from django.contrib import admin
from . import models 
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['get_first_name', 'get_last_name', 'image', 'mobile_no']
    list_display = ['first_name','last_name','mobile_no', 'image']    
    def first_name(self,obj):
        return obj.user.first_name     
    def last_name(self,obj):
        return obj.user.last_name

admin.site.register(models.UserProfile, UserAdmin)
