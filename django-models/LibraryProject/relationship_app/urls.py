from django.urls import path
from .views import list_books, LibraryDetailView, signup_view

urlpatterns = [
    path("books/", list_books, name="list_books"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
    path("signup/", signup_view, name="signup"),
]
