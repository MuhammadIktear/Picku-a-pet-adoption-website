from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.URLField(max_length=200,blank=True, null=True)
    mobile_no = models.CharField(max_length=15,blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    def __str__(self):
        return f"{self.user.username}"
    