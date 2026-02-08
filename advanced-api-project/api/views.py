"""
API Views for the Advanced API Project

This module contains ViewSets and Generic Views with advanced features:
- Filtering: Filter books by title, author, publication_year
- Searching: Search books by title and author name
- Ordering: Order books by any field

Features implemented:
- DjangoFilterBackend for precise filtering
- SearchFilter for text-based searches
- OrderingFilter for flexible sorting
"""

from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


# ==================== VIEWSETS ====================

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


# ==================== GENERIC VIEWS WITH FILTERING/SEARCHING/ORDERING ====================

class BookListView(generics.ListAPIView):
    """
    ListView: Retrieve all books with filtering, searching, and ordering
    
    Endpoint: GET /api/books/list/
    Permissions: Anyone can view (read-only)
    
    FILTERING OPTIONS:
    ==================
    Filter books by exact matches on specific fields:
    
    - By title (exact match):
      GET /api/books/list/?title=Django for Beginners
    
    - By author (ID):
      GET /api/books/list/?author=1
    
    - By publication year:
      GET /api/books/list/?publication_year=2023
    
    - Multiple filters (AND logic):
      GET /api/books/list/?author=1&publication_year=2023
    
    SEARCH FUNCTIONALITY:
    ====================
    Search across title and author name fields (partial matches):
    
    - Search in title or author name:
      GET /api/books/list/?search=Django
    
    - Search returns results that match in either field
    - Case-insensitive partial matching
    
    ORDERING OPTIONS:
    =================
    Order results by any field (ascending or descending):
    
    - Order by title (A-Z):
      GET /api/books/list/?ordering=title
    
    - Order by title (Z-A):
      GET /api/books/list/?ordering=-title
    
    - Order by publication year (oldest first):
      GET /api/books/list/?ordering=publication_year
    
    - Order by publication year (newest first):
      GET /api/books/list/?ordering=-publication_year
    
    - Multiple ordering fields:
      GET /api/books/list/?ordering=-publication_year,title
    
    COMBINED EXAMPLES:
    ==================
    
    1. Search for "Django" and order by publication year:
       GET /api/books/list/?search=Django&ordering=-publication_year
    
    2. Filter by author and order by title:
       GET /api/books/list/?author=1&ordering=title
    
    3. Filter by year, search for keyword, and order:
       GET /api/books/list/?publication_year=2023&search=REST&ordering=title
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Configure filter backends
    filter_backends = [
        DjangoFilterBackend,  # For precise field filtering
        filters.SearchFilter,  # For text search across fields
        filters.OrderingFilter,  # For sorting results
    ]
    
    # Specify which fields can be filtered (exact matches)
    filterset_fields = ['title', 'author', 'publication_year']
    
    # Specify which fields can be searched (partial matches)
    # Use '^' for starts-with, '=' for exact, '@' for full-text, '$' for regex
    search_fields = ['title', 'author__name']
    
    # Specify which fields can be used for ordering
    ordering_fields = ['title', 'publication_year', 'author__name']
    
    # Default ordering if none specified
    ordering = ['-publication_year']  # Newest books first by default


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView: Retrieve a single book by ID
    
    Endpoint: GET /api/books/detail/<int:pk>/
    Permissions: Anyone can view (read-only)
    
    Example:
    GET /api/books/detail/1/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    CreateView: Add a new book
    
    Endpoint: POST /api/books/create/
    Permissions: Only authenticated users can create
    
    Request Body Example:
    {
        "title": "Django for Beginners",
        "publication_year": 2023,
        "author": 1
    }
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """
        Custom create logic with logging
        """
        book = serializer.save()
        print(f"New book created: {book.title} by {book.author.name}")


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView: Modify an existing book
    
    Endpoint: PUT/PATCH /api/books/update/<int:pk>/
    Permissions: Only authenticated users can update
    
    Supports:
    - PUT: Full update (all fields required)
    - PATCH: Partial update (only specified fields)
    
    Example (PATCH):
    {
        "title": "Django for Advanced Users"
    }
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        """
        Custom update logic with logging
        """
        book = serializer.save()
        print(f"Book updated: {book.title}")


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView: Remove a book
    
    Endpoint: DELETE /api/books/delete/<int:pk>/
    Permissions: Only authenticated users can delete
    
    Returns: 204 No Content on success
    
    Example:
    DELETE /api/books/delete/1/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_destroy(self, instance):
        """
        Custom delete logic with logging
        """
        book_title = instance.title
        instance.delete()
        print(f"Book deleted: {book_title}")