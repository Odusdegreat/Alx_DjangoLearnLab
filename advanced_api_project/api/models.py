from django.db import models

# Author represents a writer who can have multiple books.
# One Author -> Many Books (one-to-many relationship).
class Author(models.Model):
    # Stores the author's name.
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


# Book represents a book written by exactly one Author.
class Book(models.Model):
    # Book title.
    title = models.CharField(max_length=255)

    # Year the book was published.
    publication_year = models.IntegerField()

    # ForeignKey creates one-to-many:
    # - one author can have many books
    # - deleting an author deletes their books
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
    )

    def __str__(self) -> str:
        return f"{self.title} ({self.publication_year})"
