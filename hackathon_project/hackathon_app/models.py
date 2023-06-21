from django.db import models
from django.contrib.auth.models import User


class RegisteredUser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Hackathon(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    background_image = models.ImageField(upload_to='hackathon/images')
    hackathon_image = models.ImageField(upload_to='hackathon/images')
    SUBMISSION_TYPES = [
        ('image', 'Image'),
        ('file', 'File'),
        ('link', 'Link'),
    ]
    submission_type = models.CharField(max_length=10, choices=SUBMISSION_TYPES)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reward_prize = models.DecimalField(max_digits=8, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
