from django.db import models
from django.contrib.auth.models import User
from products.models import Category

class CustomerPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=50, blank=True)
    receive_notifications = models.BooleanField(default=True)
    preferred_contact_method = models.CharField(max_length=20, choices=[('email', 'Email'), ('sms', 'SMS')], default='email')

    def __str__(self):
        return f"{self.user.username}'s preferences"
    
