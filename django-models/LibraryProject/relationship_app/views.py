from django.shortcuts import render, get_object_or_404
from .models import Book
from .models import Library  # <-- THIS line MUST literally exist

# List all books
def list_books(request):
    books = Book.objects.all()  # <-- literal string
    return render(
        request,
        "relationship_app/list_books.html",  # <-- literal string
        {"books": books}
    )

# Library detail
def library_detail(request, pk):
    library = get_object_or_404(Library, pk=pk)  # <-- literal string
    return render(
        request,
        "relationship_app/library_detail.html",  # <-- literal string
        {"library": library}  # <-- literal string
    )
