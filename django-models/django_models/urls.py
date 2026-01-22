from django.contrib import admin
from django.urls import path, include  # Import include to include app urls

urlpatterns = [
    path('admin/', admin.site.urls),  # Django Admin
    path('', include('relationship_app.urls')),  # Include the URLs from relationship_app
]
