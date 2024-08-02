from django.contrib import admin
from .models import Species, Sex, Breed, Color, Size, Pet ,Adopt,Status

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

@admin.register(Adopt)
class AdoptAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'adopt_date')
    list_filter = ('adopt_date',)
    search_fields = ('user__username', 'pet__name')