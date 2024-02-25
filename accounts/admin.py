from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser



class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = CustomUser
	list_display = ['email','first_name','last_name','phone_number','id',"is_active", 'is_superuser', 'is_staff']

	fieldsets = (
	(None, {"fields": ("email", 'first_name', 'last_name', 'phone_number', "password","image")}),
	("Permissions", {"fields": ("is_staff", "is_active")}),
	)
	add_fieldsets = (
	(None, {
	    "classes": ("wide",),
	    "fields": ("email", 'first_name', 'last_name', 'phone_number','image', "password1", "password2", "is_staff","is_active")}
	    ),)
	ordering = ['email',]

admin.site.register(CustomUser, CustomUserAdmin)
