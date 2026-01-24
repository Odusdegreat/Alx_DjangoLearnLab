from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Custom User Manager to handle user creation and superuser creation
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

# Custom User model extending AbstractUser
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)  # Optional date_of_birth field
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)  # Optional profile photo field

    # Link the CustomUserManager to the CustomUser model
    objects = CustomUserManager()

    def __str__(self):
        return self.username  # Return the username as a string representation of the user
