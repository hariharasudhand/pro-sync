from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.template import loader
from django.http import HttpResponse
from .models import Profile, Groups, RolePermission, Organization
from .forms import (OrgRegisterForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm,
                    GroupsForm, RolePermissionForm, OrgUpdateForm, OrgApprovalForm,
                    ChangePassForm)


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.profile.force_login:
                    return redirect('change-pass')

                if user.profile.status == 'INACTIVE':
                    return redirect('org-registered')

                login(request, user)
                # messages.info(request, "You are now logged in as {username}")
                return redirect('app/main.html')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="users/login.html",
                  context={"form": form})


def change_pass(request):
    user = request.user
    form = ChangePassForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            obj.force_login = False
            obj.save()
            return redirect('success')

    context = {
        'form': form,
        'model': user,
    }

    return render(request, 'users/change_pass.html', context)


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


def org_approved(request):
    org = Organization.objects.all().order_by('-date_added')
    form = OrgApprovalForm(request.POST or None)
    context = {
        'form': form,
        'model': org,
        'org_id': 0,
    }
    return render(request, 'users/org_approve.html', context)


def org_approve(request, id):
    org = Organization.objects.all().order_by('-date_added')
    form = OrgApprovalForm(request.POST or None)

    if id > 0:
        obj = Profile.objects.get(org_id=id)
        form = OrgApprovalForm(request.POST or None, instance=obj)
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
    context = {
        'form': form,
        'model': org,
        'org_id': id,
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

    context = {
        'form': form,
        'org_id': org_id,
        'org_obj': org_obj,
    }
    return render(request, 'users/org_update.html', context)


def register(request):
    org_id = request.user.profile.org.id
    org_obj = Organization.objects.get(id=org_id)
    form = UserRegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user_obj = form.save()
            messages.success(request, 'New user {user_obj.username} is created')
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
    return roles_helper(request, 0)


def roles_update(request, id):
    return roles_helper(request, id)


def roles_helper(request, id):
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
    # module = request.user.profile.group.role_permission.module
    # print('The moduels: ', module)
    # module.co
    if form.is_valid():
        form.save()
        messages.success(request, '{str_msg} data is updated')
        return redirect(str_redirect)
    context = {
        'form': form,
        'model': model,
        'is_update': is_update,
        'obj': obj,
        'org_id': org_id,
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
