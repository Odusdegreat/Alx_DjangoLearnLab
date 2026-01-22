from django.shortcuts import render
from .models import Book

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()  # Get all books
    return render(request, 'list_books.html', {'books': books})
