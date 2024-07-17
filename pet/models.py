from django.db import models
from django.contrib.auth.models import User

class Species(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=40, unique=True)
    def __str__(self):
        return self.name    

class Sex(models.Model):
    name = models.CharField(max_length=10)
    slug = models.SlugField(max_length=40, unique=True)
    def __str__(self):
        return self.name

class Breed(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=40, unique=True)
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=40, unique=True)
    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=40, unique=True)
    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=40, unique=True)
    def __str__(self):
        return self.name
    
class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.ManyToManyField(Species)
    breed = models.ManyToManyField(Breed)
    color = models.ManyToManyField(Color)
    size = models.ManyToManyField(Size)
    sex = models.ManyToManyField(Sex)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='media/pet_images/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    rehoming_fee = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    details = models.TextField()

    def __str__(self):
        return self.name 
    
class Review(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.first_name} {self.user.last_name} ; Pet {self.pet.name}"
    
class Adopt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    adopt_date = models.DateTimeField(auto_now_add=True)
