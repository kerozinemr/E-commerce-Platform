from .models import *
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group


def client_profile(created, sender, instance, **kwargs):
    if created:
        group = Group.objects.get(name ='client')
        instance.groups.add(group)
        
        Client.objects.create(
            user =instance,
            name =instance.username,
            )
        print('profile created')
        
post_save.connect(client_profile, sender=User)
        
        