"""
Unit Tests for API Views

This module contains comprehensive test cases for the Advanced API Project.
Tests cover CRUD operations, filtering, searching, ordering, permissions, and authentication.

Test Categories:
1. Book CRUD Operations
2. Filtering Functionality
3. Search Functionality
4. Ordering Functionality
5. Authentication & Permissions
6. Edge Cases & Error Handling

Run tests with: python manage.py test api
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from datetime import date
from .models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Comprehensive test suite for Book API endpoints
    
    Tests all CRUD operations, filtering, searching, ordering,
    and permission controls.
    """
    
    def setUp(self):
        """
        Set up test data and authentication
        
        Creates:
        - Test users (authenticated and unauthenticated)
        - Test authors
        - Test books
        - API client
        """
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )
        
        # Create API client
        self.client = APIClient()
        
        # Create test authors
        self.author1 = Author.objects.create(
            name='William Vincent',
            bio='Django expert and author',
            date_of_birth=date(1980, 1, 1)
        )
        
        self.author2 = Author.objects.create(
            name='Andrew Mead',
            bio='Full-stack developer',
            date_of_birth=date(1985, 5, 15)
        )
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Django for Beginners',
            publication_year=2023,
            author=self.author1
        )
        
        self.book2 = Book.objects.create(
            title='Django for Professionals',
            publication_year=2024,
            author=self.author1
        )
        
        self.book3 = Book.objects.create(
            title='Modern JavaScript',
            publication_year=2022,
            author=self.author2
        )
        
        # API endpoints
        self.list_url = '/api/books/list/'
        self.create_url = '/api/books/create/'
    
    
    # ==================== CRUD OPERATION TESTS ====================
    
    def test_get_all_books(self):
        """
        Test retrieving all books (public access)
        
        Verifies:
        - Endpoint returns 200 OK
        - All books are returned
        - Response is in correct format
        """
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        
        # Verify book data structure
        self.assertIn('id', response.data[0])
        self.assertIn('title', response.data[0])
        self.assertIn('publication_year', response.data[0])
        self.assertIn('author', response.data[0])
    
    
    def test_get_single_book(self):
        """
        Test retrieving a single book by ID
        
        Verifies:
        - Endpoint returns 200 OK
        - Correct book is returned
        - All fields are present
        """
        url = f'/api/books/detail/{self.book1.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Django for Beginners')
        self.assertEqual(response.data['publication_year'], 2023)
        self.assertEqual(response.data['author'], self.author1.id)
    
    
    def test_get_nonexistent_book(self):
        """
        Test retrieving a book that doesn't exist
        
        Verifies:
        - Endpoint returns 404 NOT FOUND
        """
        url = '/api/books/detail/9999/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    
    def test_create_book_authenticated(self):
        """
        Test creating a book with authentication
        
        Verifies:
        - Authenticated user can create a book
        - Returns 201 CREATED
        - Book is saved to database
        - Response contains correct data
        """
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'Test Book',
            'publication_year': 2024,
            'author': self.author1.id
        }
        
        response = self.client.post(self.create_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['publication_year'], 2024)
        
        # Verify book exists in database
        book = Book.objects.get(title='Test Book')
        self.assertEqual(book.publication_year, 2024)
        self.assertEqual(book.author, self.author1)
    
    
    def test_create_book_unauthenticated(self):
        """
        Test creating a book without authentication
        
        Verifies:
        - Unauthenticated user cannot create a book
        - Returns 401 UNAUTHORIZED or 403 FORBIDDEN
        - Book is not created in database
        """
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2024,
            'author': self.author1.id
        }
        
        response = self.client.post(self.create_url, data)
        
        # Should return 401 or 403
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )
        
        # Book should not be created
        self.assertEqual(Book.objects.count(), 3)
    
    
    def test_create_book_invalid_data(self):
        """
        Test creating a book with invalid data
        
        Verifies:
        - Returns 400 BAD REQUEST
        - Validation errors are returned
        - Book is not created
        """
        self.client.login(username='testuser', password='testpass123')
        
        # Invalid publication year (triggers ValidationError)
        data = {
            'title': 'Invalid Book',
            'publication_year': 3000,  # Should fail validation
            'author': self.author1.id
        }
        
        response = self.client.post(self.create_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 3)
    
    
    def test_update_book_authenticated(self):
        """
        Test updating a book with authentication (PATCH)
        
        Verifies:
        - Authenticated user can update a book
        - Returns 200 OK
        - Changes are saved to database
        """
        self.client.login(username='testuser', password='testpass123')
        
        url = f'/api/books/update/{self.book1.id}/'
        data = {
            'title': 'Updated Django for Beginners'
        }
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Django for Beginners')
        
        # Verify database was updated
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Django for Beginners')
    
    
    def test_update_book_unauthenticated(self):
        """
        Test updating a book without authentication
        
        Verifies:
        - Unauthenticated user cannot update
        - Returns 401 or 403
        - Book is not modified
        """
        url = f'/api/books/update/{self.book1.id}/'
        data = {
            'title': 'Unauthorized Update'
        }
        
        response = self.client.patch(url, data)
        
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )
        
        # Verify book was not updated
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Django for Beginners')
    
    
    def test_delete_book_authenticated(self):
        """
        Test deleting a book with authentication
        
        Verifies:
        - Authenticated user can delete a book
        - Returns 204 NO CONTENT
        - Book is removed from database
        """
        self.client.login(username='testuser', password='testpass123')
        
        url = f'/api/books/delete/{self.book1.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
        
        # Verify book no longer exists
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
    
    
    def test_delete_book_unauthenticated(self):
        """
        Test deleting a book without authentication
        
        Verifies:
        - Unauthenticated user cannot delete
        - Returns 401 or 403
        - Book is not deleted
        """
        url = f'/api/books/delete/{self.book1.id}/'
        response = self.client.delete(url)
        
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )
        
        # Verify book still exists
        self.assertEqual(Book.objects.count(), 3)
    
    
    # ==================== FILTERING TESTS ====================
    
    def test_filter_books_by_title(self):
        """
        Test filtering books by exact title
        
        Verifies:
        - Filtering returns correct results
        - Only matching books are returned
        """
        url = f'{self.list_url}?title=Django for Beginners'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django for Beginners')
    
    
    def test_filter_books_by_author(self):
        """
        Test filtering books by author ID
        
        Verifies:
        - Filtering by author returns correct books
        - Multiple books by same author are returned
        """
        url = f'{self.list_url}?author={self.author1.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verify both books are by author1
        for book in response.data:
            self.assertEqual(book['author'], self.author1.id)
    
    
    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication year
        
        Verifies:
        - Filtering by year returns correct results
        - Only books from specified year are returned
        """
        url = f'{self.list_url}?publication_year=2023'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 2023)
    
    
    def test_filter_books_multiple_criteria(self):
        """
        Test filtering with multiple criteria (AND logic)
        
        Verifies:
        - Multiple filters work together
        - Only books matching all criteria are returned
        """
        url = f'{self.list_url}?author={self.author1.id}&publication_year=2023'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django for Beginners')
    
    
    def test_filter_no_results(self):
        """
        Test filtering with criteria that match no books
        
        Verifies:
        - Empty result set is returned
        - No errors occur
        """
        url = f'{self.list_url}?publication_year=1999'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    
    # ==================== SEARCH TESTS ====================
    
    def test_search_books_by_title(self):
        """
        Test searching books by title keyword
        
        Verifies:
        - Search returns books with matching titles
        - Partial matches work (case-insensitive)
        """
        url = f'{self.list_url}?search=Django'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Both books should have "Django" in title
        for book in response.data:
            self.assertIn('Django', book['title'])
    
    
    def test_search_books_by_author_name(self):
        """
        Test searching books by author name
        
        Verifies:
        - Search works across related fields (author__name)
        - Returns books by matching authors
        """
        url = f'{self.list_url}?search=William'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Both books should be by William Vincent
        for book in response.data:
            self.assertEqual(book['author'], self.author1.id)
    
    
    def test_search_case_insensitive(self):
        """
        Test that search is case-insensitive
        
        Verifies:
        - Lowercase search matches uppercase text
        - Search functionality is case-insensitive
        """
        url = f'{self.list_url}?search=django'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    
    def test_search_no_results(self):
        """
        Test search with no matching results
        
        Verifies:
        - Empty result set for non-matching search
        - No errors occur
        """
        url = f'{self.list_url}?search=NonexistentBook'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    
    # ==================== ORDERING TESTS ====================
    
    def test_order_books_by_title_ascending(self):
        """
        Test ordering books by title (A-Z)
        
        Verifies:
        - Books are returned in alphabetical order
        - Ascending order works correctly
        """
        url = f'{self.list_url}?ordering=title'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify alphabetical order
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    
    def test_order_books_by_title_descending(self):
        """
        Test ordering books by title (Z-A)
        
        Verifies:
        - Books are returned in reverse alphabetical order
        - Descending order works correctly
        """
        url = f'{self.list_url}?ordering=-title'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify reverse alphabetical order
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    
    def test_order_books_by_publication_year_ascending(self):
        """
        Test ordering books by publication year (oldest first)
        
        Verifies:
        - Books are ordered from oldest to newest
        - Year ordering works correctly
        """
        url = f'{self.list_url}?ordering=publication_year'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify chronological order
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))
    
    
    def test_order_books_by_publication_year_descending(self):
        """
        Test ordering books by publication year (newest first)
        
        Verifies:
        - Books are ordered from newest to oldest
        - Default ordering behavior
        """
        url = f'{self.list_url}?ordering=-publication_year'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify reverse chronological order
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
    
    
    def test_default_ordering(self):
        """
        Test default ordering when no parameter is specified
        
        Verifies:
        - Default ordering is applied (-publication_year)
        - Newest books appear first by default
        """
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should be ordered by newest first (2024, 2023, 2022)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [2024, 2023, 2022])
    
    
    # ==================== COMBINED FUNCTIONALITY TESTS ====================
    
    def test_filter_search_and_order_combined(self):
        """
        Test using filtering, searching, and ordering together
        
        Verifies:
        - All three features work in combination
        - Results are filtered, searched, and ordered correctly
        """
        url = f'{self.list_url}?author={self.author1.id}&search=Django&ordering=title'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verify filtering (author1)
        for book in response.data:
            self.assertEqual(book['author'], self.author1.id)
        
        # Verify search (contains "Django")
        for book in response.data:
            self.assertIn('Django', book['title'])
        
        # Verify ordering (alphabetical)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles[0], 'Django for Beginners')
        self.assertEqual(titles[1], 'Django for Professionals')
    
    
    # ==================== PERMISSION TESTS ====================
    
    def test_list_view_public_access(self):
        """
        Test that list view is accessible without authentication
        
        Verifies:
        - Public can view books list
        - No authentication required for GET
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_detail_view_public_access(self):
        """
        Test that detail view is accessible without authentication
        
        Verifies:
        - Public can view individual books
        - No authentication required for GET
        """
        url = f'/api/books/detail/{self.book1.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_create_requires_authentication(self):
        """
        Test that create endpoint requires authentication
        
        Verifies:
        - Unauthenticated requests are rejected
        - Proper error status is returned
        """
        data = {
            'title': 'Test',
            'publication_year': 2024,
            'author': self.author1.id
        }
        response = self.client.post(self.create_url, data)
        
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )
    
    
    def test_update_requires_authentication(self):
        """
        Test that update endpoint requires authentication
        
        Verifies:
        - Unauthenticated requests are rejected
        """
        url = f'/api/books/update/{self.book1.id}/'
        data = {'title': 'New Title'}
        response = self.client.patch(url, data)
        
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )
    
    
    def test_delete_requires_authentication(self):
        """
        Test that delete endpoint requires authentication
        
        Verifies:
        - Unauthenticated requests are rejected
        """
        url = f'/api/books/delete/{self.book1.id}/'
        response = self.client.delete(url)
        
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )


class AuthorAPITestCase(APITestCase):
    """
    Test suite for Author API endpoints
    
    Tests basic CRUD operations for authors
    """
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.author = Author.objects.create(
            name='Test Author',
            bio='Test bio',
            date_of_birth=date(1990, 1, 1)
        )
    
    
    def test_get_all_authors(self):
        """Test retrieving all authors"""
        url = '/api/authors/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    
    def test_create_author_authenticated(self):
        """Test creating an author with authentication"""
        self.client.login(username='testuser', password='testpass123')
        
        url = '/api/authors/'
        data = {
            'name': 'New Author',
            'bio': 'New bio',
            'date_of_birth': '1995-05-15'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)


# Run with: python manage.py test api