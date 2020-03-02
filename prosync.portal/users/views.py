from django.shortcuts import render, redirect
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from .models import Profile, Groups, RolePermission, Organization
from .forms import (OrgRegisterForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm,
        GroupsForm, RolePermissionForm, OrgUpdateForm)

# Organization Onboard handler,
def orgRegistered(request):
    context = {}
    template = loader.get_template('users/org_register.html')
    return HttpResponse(template.render(context, request))

def save_org(user_obj, org_obj):
    profile_obj = Profile.objects.get(user_id=user_obj.id)
    profile_obj.org_id = org_obj.id
    profile_obj.save()

def orgOnboard(request):
    if request.method == 'POST':
        o_form = OrgRegisterForm(request.POST)
        u_form = UserRegisterForm(request.POST)

        if o_form.is_valid() and u_form.is_valid():
            user_obj = u_form.save()
            org_obj = o_form.save()

            save_org(user_obj, org_obj)

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
            messages.success(request, f'The Organization details are updated')
            redirect('org-update')

    context = {
        'form': form,
        'org_id': org_id,
        'org_obj': org_obj,
    }
    return render(request, 'users/org_update.html', context)

def activate(request):
    pass

def register(request):
    org_id = request.user.profile.org.id
    org_obj = Organization.objects.get(id=org_id)
    form = UserRegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user_obj = form.save()
            messages.success(request, f'New user { user_obj.username } is created')
            save_org(user_obj, org_obj)
            redirect('register')

    context = {
        'form': form,
        'org_id': org_id,
    }
    return render(request, 'users/users_add.html', context)

def profile(request):
    context = {}
    return render(request, 'users/organization_add.html', context)

def roles_add(request):
    return rolesHelper(request,0)

def roles_update(request, id):
    return rolesHelper(request, id)

def rolesHelper(request, id):
    model = RolePermission.objects.filter(status='ACTIVE')
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
    if id:
        obj = RolePermission.objects.get(id=id)
        form = RolePermissionForm(request.POST or None)

    str_render = "users/roles.html"
    return cancel_helper(request, id, model, form, obj, str_render)

def group_add(request):
    return groupsHelper(request,0)

def group_update(request, id):
    return groupsHelper(request,id)

def groups_cancel(request, id):
    model = Groups.objects.filter(status='ACTIVE')
    if id:
        obj = Groups.objects.get(id=id)
        form = Groups(request.POST or None)

    str_render = "users/groups.html"
    return cancel_helper(request, id, model, form, obj, str_render)


def groupsHelper(request, id):
    model = Groups.objects.filter(status='ACTIVE')
    if id > 0:
        obj = Groups.objects.get(id=id)
        form = GroupsForm(request.POST or None, instance=obj)
        is_update = True
    else:
        form = GroupsForm(request.POST or None)
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
        return redirect(str_redirect)
    context = {
        'form': form,
        'model': model,
        'is_update': is_update,
        'obj': obj,
        'org_id':org_id,
    }
    return render(request, str_render, context)

def cancel_helper(request, id, model, form, obj, str_render):
    if id:
        obj.status = 'INACTIVE'
        obj.save()

    context = {
        'model': model,
        'form': form
    }
    return render(request, str_render, context)