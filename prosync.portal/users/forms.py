from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import Organization, Profile

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class OrgRegisterForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ['org_name']

class OrgUpdateForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ['org_type']

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['phone', 'photo']