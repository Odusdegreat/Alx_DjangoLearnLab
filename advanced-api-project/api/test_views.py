from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Author, Book


class TestViews(APITestCase):
    def test_create_author_returns_201(self):
        url = reverse("author-list")
        res = self.client.post(url, {"name": "Chinua Achebe"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("books", res.data)

    def test_list_authors_returns_200(self):
        Author.objects.create(name="Wole Soyinka")
        url = reverse("author-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_book_returns_201(self):
        author = Author.objects.create(name="Chimamanda Adichie")
        url = reverse("book-list")
        res = self.client.post(
            url,
            {"title": "Half of a Yellow Sun", "publication_year": 2006, "author": author.id},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_future_year_returns_400(self):
        author = Author.objects.create(name="Test Author")
        url = reverse("book-list")
        future_year = timezone.now().year + 1

        res = self.client.post(
            url,
            {"title": "Future Book", "publication_year": future_year, "author": author.id},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", res.data)

    def test_author_nested_books(self):
        author = Author.objects.create(name="Nested Tester")
        Book.objects.create(title="Book One", publication_year=2000, author=author)

        url = reverse("author-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)
        self.assertIn("books", res.data[0])
