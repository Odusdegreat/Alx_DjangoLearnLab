from django.urls import path
from . import views  # Import your views

urlpatterns = [
    # Function-based view (FBV) for listing all books
    path('books/', views.list_books, name='list_books'),

    # Class-based view (CBV) for displaying library details
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]
