from django import forms

from .models import Product, Batch


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['pro_name', 'pro_price', 'exp_duration', 'status', 'org']
        # widgets = {'org_id': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)


class BatchForm(forms.ModelForm):
    # prod_id = forms.ModelChoiceField(queryset=Product.objects.all(), required=True)

    class Meta:
        model = Batch
        fields = ['batch_name', 'prod_id', 'no_of_products', 'status', 'org']

    def __init__(self, *args, **kwargs):
        super(BatchForm, self).__init__(*args, **kwargs)

        # if self.instance:
            # self.fields['prod_id'].queryset = Product.objects.filter(status__iexact='ACTIVE')
