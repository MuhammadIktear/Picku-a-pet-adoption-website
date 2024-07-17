from django.db import models

# Create your models here.
class ContactUs(models.Model):
    name=models.CharField(max_length=40)
    email=models.CharField(max_length=50)
    message=models.TextField()
    
    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural="Contact Us"