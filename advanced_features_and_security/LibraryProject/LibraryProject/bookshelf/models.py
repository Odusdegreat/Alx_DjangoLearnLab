from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)  # Optional: Date of birth field
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)  # Optional: Profile photo field

    def __str__(self):
        return self.username  # Return the username as a string representation of the user
