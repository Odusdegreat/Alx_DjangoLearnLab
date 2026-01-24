from django.db import models
from django.contrib.auth.models import User

# Define choices for user roles
class Role(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    MEMBER = 'Member', 'Member'

# UserProfile model that extends the User model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # Link to the built-in User model
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)  # Role choices: Admin or Member
    bio = models.TextField(blank=True, null=True)  # Optional field for a short bio
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Optional field for profile picture
    
    def __str__(self):
        return f"{self.user.username}'s Profile"  # Return a string representation of the profile

