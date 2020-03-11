from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.template import loader
from django.http import HttpResponse
from .models import Profile, Groups, RolePermission, Organization
from .forms import (OrgRegisterForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm,
                    GroupsForm, RolePermissionForm, OrgUpdateForm, OrgApprovalForm,
                    ProfileAddForm)
from app.utils import AccessPermission


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.profile.status == 'INACTIVE':
                    return redirect('org-registered')

                login(request, user)

                if user.profile.force_login:
                    save_org(user, user.profile.org)
                    return redirect('password_change')

                if not user.is_superuser:
                    roles = AccessPermission(user.profile.group.role_permission)
                else:
                    roles = 'superuser'
                context = {
                    'roles': roles,
                }
                return render(request, 'app/main.html', context)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="users/login.html",
                  context={"form": form})


# Organization Onboard handler,
def org_registered(request):
    context = {}
    logout(request)
    template = loader.get_template('users/org_register.html')
    return HttpResponse(template.render(context, request))


def save_org(user_obj, org_obj):
    profile_obj = Profile.objects.get(user_id=user_obj.id)
    profile_obj.org_id = org_obj.id
    profile_obj.force_login = False
    profile_obj.save()

def create_admin_group(org_id):
    role = RolePermission.objects.get(org = org_id)
    group = Groups.objects.get(org = org_id)
    role.id = 1
    role.org = org_id
    role.role_name = "Administrator"
    role.module = ('Admin','Product','Billing','Batch','Support','Offer')
    role.create = True
    role.view = True
    role.update = True
    role.delete = True

    group.id = 1
    group.org = org_id


def org_approved(request):
    org = Organization.objects.all().order_by('-date_added')
    form = OrgApprovalForm(request.POST or None)
    if not request.user.is_superuser:
        roles = AccessPermission(request.user.profile.group.role_permission)
    else:
        roles = 'SuperUser'
    context = {
        'form': form,
        'model': org,
        'org_id': 0,
        'roles': roles,
    }
    return render(request, 'users/org_approve.html', context)


def org_approve(request, id):
    print('1......', id)
    if id > 0:
        print('4......')
        obj = Profile.objects.get(org_id=id)
        print('5......')
        org_id = obj.org.id
        print('6......', org_id)
        form = OrgApprovalForm(org_id, request.POST or None, instance=obj)
        print('7......')
        if request.method == 'POST':
            if form.is_valid():
                prof_obj = form.save()
                prof_obj.group = form.cleaned_data.get('group')
                prof_obj.status = 'ACTIVE'
                prof_obj.force_login = False
                prof_obj.save()
                org_obj = Organization.objects.get(id=prof_obj.org_id)
                org_obj.status = 'ACTIVE'
                org_obj.save()
                messages.success(request, 'The organization is activated')
                return redirect('org-approved')
    else:
        print('2......')
        form = OrgApprovalForm(request.POST or None)
    if not request.user.is_superuser:
        roles = AccessPermission(request.user.profile.group.role_permission)
    else:
        roles = 'Superuser'

    org = Organization.objects.filter(status='INACTIVE').order_by('-date_added')
    context = {
        'form': form,
        'model': org,
        'org_id': id,
        'roles': roles,
    }
    return render(request, 'users/org_approve.html', context)


def org_onboard(request):
    if request.method == 'POST':
        o_form = OrgRegisterForm(request.POST)
        u_form = UserRegisterForm(request.POST)

        if o_form.is_valid() and u_form.is_valid():
            user_obj = u_form.save()
            org_obj = o_form.save()

            save_org(user_obj, org_obj)
            messages.success(request, "The organization is activated")
            return redirect('org-registered')
    else:
        o_form = OrgRegisterForm(request.POST or None)
        u_form = UserRegisterForm(request.POST or None)

    context = {
        'o_form': o_form,
        'u_form': u_form
    }
    return render(request, 'users/organization_add.html', context)


def org_update(request):
    org_id = request.user.profile.org.id
    org_obj = Organization.objects.get(id=org_id)
    form = OrgUpdateForm(request.POST or None, instance=org_obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'The Organization details are updated')
            redirect('org-update')
    roles = AccessPermission(request.user.profile.group.role_permission)
    context = {
        'form': form,
        'org_id': org_id,
        'org_obj': org_obj,
        'roles': roles,
    }
    return render(request, 'users/org_update.html', context)


def register(request):
    org_id = request.user.profile.org.id
    org_obj = Organization.objects.get(id=org_id)
    form = UserRegisterForm(request.POST or None)
    p_form = ProfileAddForm(org_id, request.POST or None)
    is_update = False
    if request.method == 'POST' and form.is_valid() and p_form.is_valid():
        user_obj = form.save()
        messages.success(request, f'New user {user_obj.username} is created')
        profile_obj = Profile.objects.get(user_id=user_obj.id)
        profile_obj.org_id = org_obj.id
        profile_obj.group = p_form.cleaned_data.get('group')
        profile_obj.status = 'ACTIVE'
        profile_obj.force_login = True
        profile_obj.save()
        redirect('register')
    return profile_helper(request, form, p_form, org_id, is_update)


def profile_update(request, id):
    org_id = request.user.profile.org.id
    is_update = True
    if id:
        u_obj = User.objects.get(id=id)
        p_obj = Profile.objects.get(user_id=id)
        u_form = UserRegisterForm(request.POST or None, instance=u_obj)
        p_form = ProfileAddForm(org_id, request.POST or None, instance=p_obj)

        if request.method == 'POST' and u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f' {username} profile is updated')
        return profile_helper(request, u_form, p_form, org_id, is_update)

def profile_helper(request, u_form, p_form, org_id, is_update):
    model = User.objects.filter(profile__org=org_id)
    roles = AccessPermission(request.user.profile.group.role_permission)
    context = {
        'form': u_form,
        'model': model,
        'p_form': p_form,
        'org_id': org_id,
        'roles': roles,
        'is_update': is_update,
    }
    return render(request, 'users/users_add.html', context)

def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile is updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    roles = AccessPermission(request.user.profile.group.role_permission)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'roles': roles,
    }
    return render(request, 'users/profile.html', context)

def profile_delete(request, id):
    pass

def roles_add(request):
    return roles_helper(request, 0)

def roles_update(request, id):
    return roles_helper(request, id)


def roles_helper(request, id):
    orgId = request.user.profile.org.id
    model = RolePermission.objects.filter(status='ACTIVE').filter(org_id=orgId)
    if id > 0:
        obj = RolePermission.objects.get(id=id)
        form = RolePermissionForm(request.POST or None, instance=obj)
        is_update = True
    else:
        form = RolePermissionForm(request.POST or None)
        is_update = False
        obj = None

    str_redirect = 'roles'
    str_render = 'users/roles.html'
    str_msg = 'Roles'
    return helper(request, model, form, str_redirect, str_render, str_msg, is_update, obj)


def roles_cancel(request, id):
    model = RolePermission.objects.filter(status='ACTIVE')
    form = RolePermissionForm(request.POST or None)
    if id:
        obj = RolePermission.objects.get(id=id)

    str_render = "users/roles.html"
    return cancel_helper(request, id, model, form, obj, str_render)


def group_add(request):
    return groups_helper(request, 0)


def group_update(request, id):
    return groups_helper(request, id)


def groups_cancel(request, id):
    model = Groups.objects.filter(status='ACTIVE')
    form = Groups(request.POST or None)
    if id:
        obj = Groups.objects.get(id=id)

    str_render = "users/groups.html"
    return cancel_helper(request, id, model, form, obj, str_render)


def groups_helper(request, id):
    orgId = request.user.profile.org.id
    model = Groups.objects.filter(status='ACTIVE').filter(org=orgId)
    if id > 0:
        obj = Groups.objects.get(id=id)
        form = GroupsForm(orgId, request.POST or None, instance=obj)
        is_update = True
    else:
        form = GroupsForm(orgId, request.POST or None)
        is_update = False
        obj = None

    str_redirect = 'groups'
    str_render = 'users/groups.html'
    str_msg = 'Groups'
    return helper(request, model, form, str_redirect, str_render, str_msg, is_update, obj)


def helper(request, model, form, str_redirect, str_render, str_msg, is_update, obj):
    org_id = request.user.profile.org.id
    if form.is_valid():
        form.save()
        messages.success(request, f'{str_msg} data is updated')

    roles = AccessPermission(request.user.profile.group.role_permission)
    context = {
        'form': form,
        'model': model,
        'is_update': is_update,
        'obj': obj,
        'org_id': org_id,
        'roles': roles,
    }
    return render(request, str_render, context)


def cancel_helper(request, id, model, form, obj, str_render):
    if id:
        obj.status = 'INACTIVE'
        obj.save()
    roles = AccessPermission(request.user.profile.group.role_permission)
    context = {
        'model': model,
        'form': form,
        'roles': roles,
    }
    return render(request, str_render, context)
