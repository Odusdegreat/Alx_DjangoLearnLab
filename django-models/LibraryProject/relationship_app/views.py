from django.shortcuts import render
from .models import Book

def list_books(request):
    # Fetch all books
    books = Book.objects.all()  # <-- MUST have this exact line

    # Render template
    return render(
        request,
        "relationship_app/list_books.html",  # <-- MUST have this exact string
        {"books": books}
    )
