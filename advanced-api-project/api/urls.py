"""
URL Configuration for the API

This module defines URL patterns for both ViewSets (using routers)
and Generic Views (using path()).

URL Structure:
- /api/authors/ - Author ViewSet (full CRUD via router)
- /api/books/ - Book ViewSet (full CRUD via router)
- /api/books/list/ - List all books (Generic ListView)
- /api/books/<int:pk>/ - Book detail (Generic DetailView)
- /api/books/create/ - Create new book (Generic CreateView)
- /api/books/<int:pk>/update/ - Update book (Generic UpdateView)
- /api/books/<int:pk>/delete/ - Delete book (Generic DeleteView)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthorViewSet,
    BookViewSet,
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

# ==================== ROUTER SETUP ====================
# Router automatically generates URL patterns for ViewSets
router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')

# ==================== URL PATTERNS ====================
urlpatterns = [
    # Include router URLs for ViewSets
    # This creates endpoints like:
    # - GET/POST /api/authors/
    # - GET/PUT/PATCH/DELETE /api/authors/<pk>/
    # - GET/POST /api/books/
    # - GET/PUT/PATCH/DELETE /api/books/<pk>/
    path('', include(router.urls)),
    
    # ==================== GENERIC VIEWS ENDPOINTS ====================
    
    # ListView: GET all books
    # Endpoint: /api/books/list/
    # Permissions: Anyone (read-only)
    # Returns: List of all books
    path('books/list/', BookListView.as_view(), name='book-list'),
    
    # DetailView: GET a single book by ID
    # Endpoint: /api/books/<int:pk>/
    # Permissions: Anyone (read-only)
    # Returns: Single book details
    # Note: This might conflict with router, use books/detail/<pk>/ if needed
    path('books/detail/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # CreateView: POST to create a new book
    # Endpoint: /api/books/create/
    # Permissions: Authenticated users only
    # Request Body: {"title": "...", "publication_year": ..., "author": ...}
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # UpdateView: PUT/PATCH to update an existing book
    # Endpoint: /api/books/<int:pk>/update/
    # Permissions: Authenticated users only
    # Request Body: Full object (PUT) or partial (PATCH)
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),
    
    # DeleteView: DELETE to remove a book
    # Endpoint: /api/books/<int:pk>/delete/
    # Permissions: Authenticated users only
    # Returns: 204 No Content on success
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
]