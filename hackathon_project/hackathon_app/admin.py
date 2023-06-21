from django.contrib import admin
from .models import RegisteredUser, Hackathon

# Register your models here.
admin.site.register(RegisteredUser)
admin.site.register(Hackathon)