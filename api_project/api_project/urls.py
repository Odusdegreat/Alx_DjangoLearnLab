from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),

    # Token auth endpoint (username + password -> token)
    path('api/token/', obtain_auth_token, name='api-token'),

    # Your API app routes
    path('api/', include('api.urls')),
]
