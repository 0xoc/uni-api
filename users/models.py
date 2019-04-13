from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")

    # todo: other login info

    def __str__(self):
        return str(self.user)


class Student(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="student")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)