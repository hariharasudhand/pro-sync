from __future__ import unicode_literals

import jsonfield    # install django-jsonfield for mysql
from django.db import models
from users.models import Organization
# from django.contrib.postgres.fields import JSONField      # import JSONField and create 'prod_id_json = JSONField()'


class Batch(models.Model):
    batch_name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    batch_code = models.BigIntegerField()
    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    prod_id = models.BigIntegerField()
    no_of_products = models.BigIntegerField()
    batch_date = models.DateField(auto_now_add=True)
    exp_date = models.DateField()
    release_date = models.DateField()
    status = models.CharField(max_length=10, null=False, blank=False, default='ACTIVE')
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    prod_id_json = jsonfield.JSONField()


class Product(models.Model):
    pro_name = models.CharField(max_length=50, null=False, blank=False)
    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)
    pro_price = models.BigIntegerField()
    exp_duration = models.BigIntegerField()
    status = models.CharField(max_length=10, null=False, blank=False, default='ACTIVE')
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)


