from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Follow, Notification, Profile, Equipment, History


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Equipment)
def log_item(sender, instance, created, **kwargs):
    if created:
        History.objects.create(user=instance.author, action=f"Added item {instance.name}")
    else:
        History.objects.create(user=instance.author, action=f"Updated item {instance.name}")

@receiver(post_save, sender=Equipment)
def notify_followers(sender, instance, created, **kwargs):
    if created:
        followers = Follow.objects.filter(following=instance.author)
        for f in followers:
            Notification.objects.create(
                user=f.follower,
                message=f"Пользователь {instance.author.username} добавил новый объект {instance.name}"
            )