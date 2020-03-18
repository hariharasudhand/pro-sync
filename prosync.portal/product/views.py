from django.shortcuts import render, redirect
from django.core import signing
from datetime import timedelta
from app.utils import AccessPermission
import json

from .forms import ProductForm, BatchForm
from .models import Product, Batch
from users.views import get_roles


def product(request):
    return product_helper(request, 0, False)


def update_product(request, id):
    return product_helper(request, id, False)


def view_product(request, id):
    return product_helper(request, id, True)


def cancel_product(request, id):
    org_id = request.user.profile.org.id
    model = Product.objects.filter(status='ACTIVE', org_id=org_id)
    if id:
        obj = Product.objects.get(id=id)
        form = ProductForm(request.POST or None)

    str_redirect = 'product'
    str_render = "product/add_products.html"
    return cancel_helper(request, id, model, form, obj, str_redirect, str_render, org_id)


def product_helper(request, id, is_view):
    org_id = request.user.profile.org.id
    model = Product.objects.filter(status='ACTIVE', org_id=org_id)
    if id > 0:
        obj = Product.objects.get(id=id)
        form = ProductForm(request.POST or None, instance=obj)
        is_update = True
        if is_view:
            form.fields['pro_name'].widget.attrs['readonly'] = True
            form.fields['pro_price'].widget.attrs['readonly'] = True
            form.fields['exp_duration'].widget.attrs['readonly'] = True
            form.fields['status'].widget.attrs['readonly'] = True
            is_update = False
    else:
        form = ProductForm(request.POST or None)
        is_update = False
        obj = None

    str_redirect = 'product'
    str_render = "product/add_products.html"
    return helper(request, model, form, str_redirect, str_render, is_update, is_view, obj, org_id)


def helper(request, model, form, str_redirect, str_render, is_update, is_view, obj, org_id):
    if form.is_valid():
        form.save()
        return redirect(str_redirect)

    goto_div = False
    if is_update or is_view:
        goto_div = True

    context = {
        'form': form,
        'model': model,
        'is_update': is_update,
        'is_view': is_view,
        'obj': obj,
        'org_id': org_id,
        'goto_div': goto_div,
        'roles': get_roles(request),
    }
    return render(request, str_render, context)


def cancel_helper(request, id, model, form, obj, str_redirect, str_render, org_id):
    if id:
        obj.status = 'INACTIVE'
        obj.save()
        return redirect(str_redirect)

    context = {
        'model': model,
        'form': form,
        'org_id': org_id,
        'roles': get_roles(request),
    }
    return render(request, str_render, context)


def batch(request):
    org_id = request.user.profile.org.id
    model = Batch.objects.filter(status='ACTIVE', org_id=org_id)
    p_model = Product.objects.filter(status='ACTIVE', org_id=org_id, batch_id__isnull=True)
    form = BatchForm(request.POST or None)
    id=0
    str_redirect = 'batch'
    str_render = "product/add_batch.html"
    return batch_helper(request, id, model, p_model, form, str_redirect, str_render, org_id, is_view=False)


def view_batch(request, id):
    org_id = request.user.profile.org.id
    model = Batch.objects.filter(status='ACTIVE', org_id=org_id)
    p_model = Product.objects.filter(status='ACTIVE', org_id=org_id, batch_id__isnull=True)
    obj = Batch.objects.get(id=id)
    form = BatchForm(request.POST or None, instance=obj)
    form.fields['batch_name'].widget.attrs['readonly'] = True
    form.fields['no_of_products'].widget.attrs['readonly'] = True
    form.fields['release_date'].widget.attrs['readonly'] = True
    str_redirect = 'batch'
    str_render = "product/add_batch.html"
    return batch_helper(request, id, model, p_model, form, str_redirect, str_render, org_id, is_view=True)


def batch_helper(request, id, model, p_model, form, str_redirect, str_render, org_id, is_view):
    if form.is_valid():
        s_form = form.save()
        bat = Batch.objects.get(id=s_form.id)
        bat.batch_code = s_form.id

        prod_id = request.POST['prod_id']
        prod = Product.objects.get(id=prod_id)
        prod.batch_id = s_form.id

        # data = serializers.serialize('json', Product.objects.filter(status='ACTIVE',
        # org_id=request.user.profile.org.id), fields=('pro_name', 'pro_price'))
        barcode = ['b0'+str(i) for i in range(1, s_form.no_of_products+1)]
        data = {"product_id": prod.id, "product_name": prod.pro_name, "barcode_id": barcode}
        bat.prod_id_json = json.dumps(data)

        bat.exp_date = s_form.batch_date+timedelta(days=prod.exp_duration)

        prod.save()
        bat.save()

        return redirect(str_redirect)

    context = {
        'model': model,
        'form': form,
        'p_model': p_model,
        'org_id': org_id,
        'prod': Product.objects.filter(status='ACTIVE', org_id=org_id),
        'roles': get_roles(request),
        'is_view': is_view,
    }
    if is_view:
        context['prod_name'] = Product.objects.get(batch_id=id)
    return render(request, str_render, context)