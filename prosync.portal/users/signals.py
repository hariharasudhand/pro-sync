from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from gentelella.users.models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print('profile created: {}',Profile)
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    print('profile saved: {}', Profile)
    instance.profile.save()