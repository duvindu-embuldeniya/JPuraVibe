from django.db.models.signals import post_save, post_delete
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        user = instance
        Profile.objects.create(user = instance)

        subject = "Welcome"
        message = "We are glad you are here!"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
            )


def delete_user(sender, instance, *args, **kwargs):
    instance.user.delete()


post_save.connect(create_profile, sender = User)
post_delete.connect(delete_user, sender = Profile)