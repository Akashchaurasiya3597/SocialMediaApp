from django import forms
from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
    UserChangeForm as BaseUserChangeForm)
from CodeNicelyApp.models import User,Post,Profile
from django.contrib.auth.forms import UserCreationForm


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = ['full_name', 'email', 'phone_number', 'password']


class UserStandardCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        error_messages = {
            'phone_number': {
                'duplicate_phone_number': 'There is a user with the same contact no'
            },
        }
        fields = ('full_name', 'email', 'phone_number')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image','caption']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_image','address','cover_photos']

