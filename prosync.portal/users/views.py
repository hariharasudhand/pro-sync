from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Profile
from .forms import OrgRegisterForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Organization Onboard handler
def orgRegistered(request):
    context = {}
    template = loader.get_template('users/org_register.html')
    return HttpResponse(template.render(context, request))

def orgOnboard(request):
    if request.method == 'POST':
        o_form = OrgRegisterForm(request.POST)
        u_form = UserRegisterForm(request.POST)

        if o_form.is_valid() and u_form.is_valid():
            user_obj = u_form.save()
            org_obj = o_form.save()

            profile_obj = Profile.objects.get(user_id=user_obj.id)
            profile_obj.org_id = org_obj.id
            profile_obj.save()

            return redirect('org-registered')
    else:
        o_form = OrgRegisterForm(request.POST or None)
        u_form = UserRegisterForm(request.POST or None)

    context = {
        'o_form': o_form,
        'u_form': u_form
    }
    return render(request, 'users/organization_add.html', context)

def register(request):
    context = {}
    return render(request, 'users/organization_add.html', context)

def profile(request):
    context = {}
    return render(request, 'users/organization_add.html', context)
