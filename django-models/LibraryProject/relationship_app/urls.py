from django.urls import path
from .views import library_detail

urlpatterns = [
    path("library/<int:pk>/", library_detail, name="library_detail"),
]
