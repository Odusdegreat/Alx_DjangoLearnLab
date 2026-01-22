from django.test import TestCase
from .models import Author, Book

class AuthorModelTest(TestCase):
    def test_string_representation(self):
        author = Author(name="J.K. Rowling")
        self.assertEqual(str(author), author.name)

class BookModelTest(TestCase):
    def test_book_author_relationship(self):
        author = Author.objects.create(name="J.K. Rowling")
        book = Book.objects.create(title="Harry Potter", author=author)
        self.assertEqual(book.author.name, "J.K. Rowling")
