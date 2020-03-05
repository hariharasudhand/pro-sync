from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import Organization, Profile, RolePermission, Groups, MODULES
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ChangePassForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {'username': forms.HiddenInput(), }



class OrgRegisterForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ['org_name']


class OrgApprovalForm(forms.ModelForm):
    # org = forms.ModelChoiceField(queryset=Organization.objects.all(),
    #                                required=True)
    class Meta:
        model = Profile
        fields = ['group', 'org']
        widgets = {'org': forms.HiddenInput(), }

class OrgUpdateForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ['address', 'org_type']
        widgets = {'address': forms.Textarea(attrs={"rows":5, "cols":20}), }

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['phone', 'photo']


class RolePermissionForm(forms.ModelForm):
    module = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=MODULES)
    class Meta:
        model = RolePermission
        fields = ['role_name', 'module', 'create', 'view', 'update', 'delete', 'org']
        widgets = {'org': forms.HiddenInput(), }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # if self.instance:  # Editing and existing instance
        #     self.fields['status'].queryset = RolePermission.objects.filter(status__iexact='ACTIVE')

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'role_name',
            'module',
            # Row(
            #     Column('role_name', css_class='form-group col-md-6 mb-0'),
            #     Column('module', css_class='form-group col-md-6 mb-0'),
            #     css_class='form-row'
            # ),
            Row(
                Column('create', css_class='form-group col-md-3 mb-0'),
                Column('view', css_class='form-group col-md-3 mb-0'),
                Column('update', css_class='form-group col-md-3 mb-0'),
                Column('delete', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )


class GroupsForm(forms.ModelForm):

    class Meta:
        model = Groups
        fields = ['group_name', 'role_permission', 'org']
        widgets = {'org': forms.HiddenInput(), }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields['role_permission'].queryset = RolePermission.objects.filter(status__iexact='ACTIVE')


        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('group_name', css_class='form-group col-md-6 mb-0'),
                Column('role_permission', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )
