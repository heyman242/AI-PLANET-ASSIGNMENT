from django.db import models

# Create your models here.
class RegisteredUser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name
