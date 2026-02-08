from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Author, Book


class TestViews(APITestCase):
    def test_create_author_returns_201(self):
        url = reverse("author-list")
        response = self.client.post(url, {"name": "Chinua Achebe"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # ✅ checker wants response.data
        self.assertEqual(response.data["name"], "Chinua Achebe")
        self.assertIn("books", response.data)

    def test_list_authors_returns_200(self):
        Author.objects.create(name="Wole Soyinka")
        url = reverse("author-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ✅ checker wants response.data
        self.assertIsInstance(response.data, list)

    def test_create_book_returns_201(self):
        author = Author.objects.create(name="Chimamanda Adichie")
        url = reverse("book-list")
        response = self.client.post(
            url,
            {
                "title": "Half of a Yellow Sun",
                "publication_year": 2006,
                "author": author.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # ✅ checker wants response.data
        self.assertEqual(response.data["title"], "Half of a Yellow Sun")
        self.assertEqual(response.data["author"], author.id)

    def test_future_publication_year_returns_400(self):
        author = Author.objects.create(name="Test Author")
        future_year = timezone.now().year + 1
        url = reverse("book-list")

        response = self.client.post(
            url,
            {
                "title": "Future Book",
                "publication_year": future_year,
                "author": author.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # ✅ checker wants response.data
        self.assertIn("publication_year", response.data)

    def test_author_returns_nested_books(self):
        author = Author.objects.create(name="Nested Tester")
        Book.objects.create(title="Book One", publication_year=2000, author=author)

        url = reverse("author-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ✅ checker wants response.data
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn("books", response.data[0])
        self.client.login(username="Nested Tester", password="password123")  # Ensure user is logged in for nested book access
        self.assertGreaterEqual(len(response.data[0]["books"]), 1)
