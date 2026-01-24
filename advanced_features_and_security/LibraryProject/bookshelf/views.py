from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from .models import Book

# View to list all books (only users with 'can_view' permission can access it)
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to list all books in the database.
    This view is only accessible to users with the 'can_view' permission.
    """
    books = Book.objects.all()  # Fetch all books from the database
    return render(request, 'book_list.html', {'books': books})  # Pass books to the template
