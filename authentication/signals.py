from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CustomUser, Address


# 1️⃣ Create Address
@receiver(post_save, sender=CustomUser)
def create_user_address(sender, instance, created, **kwargs):
    print("Creating user address...")
    if created and not instance.address:
        address = Address.objects.create()
        instance.address = address
        instance.save()
