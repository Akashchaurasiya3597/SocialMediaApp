from django.contrib import admin
from CodeNicelyApp.models import User, Post, Friend, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserStandardCreationForm


# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'phone_number')
    list_filter = ('email',)
    fieldsets = ((None, {'fields': ('phone_number', 'username', 'password', 'email', 'is_staff')}),)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password')}
         ),
    )
    ordering = ('email',)
    form = UserChangeForm
    add_form = UserStandardCreationForm

    filter_horizontal = ()


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Friend)
admin.site.register(Profile)
