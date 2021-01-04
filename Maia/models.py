from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    questionaire_answered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile.objects.create(user=instance)
    instance.user_profile.save()
