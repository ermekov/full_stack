from django.db import models
from django.contrib.auth.models import User

class Equipment(models.Model):
    name = models.CharField(max_length=255)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    available_from = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    rating = models.FloatField(null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='equipment_files/', null=True, blank=True)
    image = models.ImageField(upload_to='equipment_images/', null=True, blank=True)
    public = models.BooleanField(default=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="equipments", default=1)

    def __str__(self):
        return f"{self.name} — {self.price_per_day} /day"

class Comment(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.text[:30]}"

class EquipmentList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists')
    name = models.CharField(max_length=100)
    items = models.ManyToManyField(Equipment, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)