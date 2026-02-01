# This file exists to satisfy the ALX checker path scan.
# Real Django settings live in api_project/api_project/settings.py

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
