"""
API Views for the Advanced API Project

This module contains both ViewSets and Generic Views for handling
CRUD operations on Author and Book models.

Generic Views Used:
- ListAPIView: Retrieve all books
- RetrieveAPIView: Retrieve a single book by ID
- CreateAPIView: Create a new book
- UpdateAPIView: Update an existing book
- DestroyAPIView: Delete a book
"""

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework as filters
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


# ==================== VIEWSETS ====================
# These provide a complete set of CRUD operations in a single class

class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Author instances.
    
    Provides: list, create, retrieve, update, destroy actions
    Permissions: Authenticated users can write, all can read
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Book instances.
    
    Provides: list, create, retrieve, update, destroy actions
    Permissions: Authenticated users can write, all can read
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ==================== GENERIC VIEWS FOR BOOKS ====================
# These provide more granular control over each CRUD operation

class BookListView(generics.ListAPIView):
    """
    ListView: Retrieve all books
    
    Endpoint: GET /api/books/list/
    Permissions: Anyone can view (read-only)
    Features:
    - Returns a list of all books in the database
    - Supports filtering and ordering (can be extended)
    - No authentication required for reading
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Anyone can read
    
    def get_queryset(self):
        """
        Optionally filter books by publication year or author
        Usage: /api/books/list/?publication_year=2020
        """
        queryset = Book.objects.all()
        
        # Filter by publication year if provided
        publication_year = self.request.query_params.get('publication_year', None)
        if publication_year is not None:
            queryset = queryset.filter(publication_year=publication_year)
        
        # Filter by author if provided
        author_id = self.request.query_params.get('author', None)
        if author_id is not None:
            queryset = queryset.filter(author_id=author_id)
        
        return queryset.order_by('-publication_year')  # Order by newest first


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView: Retrieve a single book by ID
    
    Endpoint: GET /api/books/<int:pk>/
    Permissions: Anyone can view (read-only)
    Features:
    - Returns detailed information about a specific book
    - Accessed via primary key (pk) in URL
    - No authentication required for reading
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Anyone can read


class BookCreateView(generics.CreateAPIView):
    """
    CreateView: Add a new book
    
    Endpoint: POST /api/books/create/
    Permissions: Only authenticated users can create
    Features:
    - Creates a new book instance
    - Validates data using BookSerializer
    - Requires authentication
    - Automatically handles validation errors
    
    Request Body Example:
    {
        "title": "Django for Beginners",
        "publication_year": 2023,
        "author": 1
    }
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Must be logged in to create
    
    def perform_create(self, serializer):
        """
        Custom create logic - can be extended to add additional fields
        or perform custom actions when a book is created
        """
        # Save the book instance
        book = serializer.save()
        
        # You can add custom logic here, such as:
        # - Logging the creation
        # - Sending notifications
        # - Setting default values
        print(f"New book created: {book.title} by {book.author.name}")


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView: Modify an existing book
    
    Endpoint: PUT/PATCH /api/books/<int:pk>/update/
    Permissions: Only authenticated users can update
    Features:
    - Updates an existing book instance
    - Supports both PUT (full update) and PATCH (partial update)
    - Validates data using BookSerializer
    - Requires authentication
    
    Request Body Example (PATCH):
    {
        "title": "Django for Advanced Users"
    }
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Must be logged in to update
    
    def perform_update(self, serializer):
        """
        Custom update logic - can be extended to perform
        additional actions when a book is updated
        """
        # Save the updated book instance
        book = serializer.save()
        
        # You can add custom logic here, such as:
        # - Logging the update
        # - Sending notifications
        # - Updating related models
        print(f"Book updated: {book.title}")


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView: Remove a book
    
    Endpoint: DELETE /api/books/<int:pk>/delete/
    Permissions: Only authenticated users can delete
    Features:
    - Deletes a book instance from the database
    - Requires authentication
    - Returns 204 No Content on success
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Must be logged in to delete
    
    def perform_destroy(self, instance):
        """
        Custom delete logic - can be extended to perform
        cleanup or validation before deletion
        """
        book_title = instance.title
        
        # Perform the deletion
        instance.delete()
        
        # You can add custom logic here, such as:
        # - Logging the deletion
        # - Cleaning up related data
        # - Sending notifications
        print(f"Book deleted: {book_title}")