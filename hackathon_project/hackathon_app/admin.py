from django.contrib import admin
from .models import RegisteredUser, Hackathon, Submission, EnrolledHackathon

# Register your models here.
admin.site.register(RegisteredUser)
admin.site.register(Hackathon)
admin.site.register(Submission)
admin.site.register(EnrolledHackathon)