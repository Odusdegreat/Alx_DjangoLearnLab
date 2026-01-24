from django.db import models
from django.contrib.auth.models import User
from .models import Library  # Assuming Library model is already defined

# Define the Librarian model
class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='librarian')  # Link to User model
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')  # Link to Library model
    is_active = models.BooleanField(default=True)  # Is the librarian currently active
    date_joined = models.DateField(auto_now_add=True)  # Date when the librarian joined

    def __str__(self):
        return f"Librarian: {self.user.username} for Library: {self.library.name}"

