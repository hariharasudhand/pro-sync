from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save

MODULES = ( ('Admin', 'Admin'), ('Product', 'Product'), ('Billing', 'Billing'),
            ('Batch', 'Batch'), ('Support', 'Support'), ('Offer', 'Offer') )
ORG_TYPE = ( ('Manufacturer', 'Manufacturer'), ('SuperStockist', 'Super Stockist'),
             ('Stockist', 'Stockist'), ('Retailer', 'Retailer') )


class Organization(models.Model):
    org_name = models.CharField(max_length=50, null=False, blank=False, default='')
    address = models.CharField(max_length=250, null=True, blank=True)
    org_type = models.CharField(max_length=20, choices=ORG_TYPE, default='Retailer')
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, null=False, blank=False, default='INACTIVE')
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.org_name

class Profile(models.Model):
    email = models.CharField(max_length=50, null=False, blank=False, default='')
    phone = models.CharField(max_length=10, null=True, blank=True)
    photo = models.ImageField(default='male_default.png', upload_to='profile_pics')
    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    user_token = models.CharField(max_length=80, null=True, blank=True)
    status = models.CharField(max_length=20, null=False, blank=False, default='INACTIVE')
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.email


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()