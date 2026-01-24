from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view to list all books
def list_books(request):
    """
    Function-based view that lists all books in the database.
    """
    books = Book.objects.all()  # Fetch all books from the database
    return render(request, 'relationship_app/list_books.html', {'books': books})  # Render the template with books data


class LibraryDetailView(DetailView):
    """
    Class-based view using DetailView to display library details.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
