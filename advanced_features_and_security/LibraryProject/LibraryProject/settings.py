# settings.py

# Add the following line to point to the custom user model:
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# Other settings
INSTALLED_APPS = [
    # Default apps...
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Add your app here
    'bookshelf',  # Make sure 'bookshelf' is listed in INSTALLED_APPS
]

# Other settings...
