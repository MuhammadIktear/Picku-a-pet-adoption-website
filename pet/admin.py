from django.contrib import admin
from .models import Species, Sex, Breed, Color, Size, Pet ,Review,Adopt,Status

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  
    
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}      

@admin.register(Sex)
class SexAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  
    
@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  
    
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  
    
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  
    

admin.site.register(Pet)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pet', 'user', 'name', 'email', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('pet__name', 'user__username', 'name', 'email')

@admin.register(Adopt)
class AdoptAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'adopt_date')
    list_filter = ('adopt_date',)
    search_fields = ('user__username', 'pet__name')