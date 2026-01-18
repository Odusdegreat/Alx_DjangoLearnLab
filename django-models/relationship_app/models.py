from django.db import models

# =====================================
# MODEL 1: AUTHOR
# =====================================
class Author(models.Model):
    """
    Represents an author who writes books.
    This is the "one" side of the one-to-many relationship with Book.
    """
    name = models.CharField(max_length=200)
    
    def __str__(self):
        # This makes it show the author's name instead of "Author object (1)"
        return self.name


# =====================================
# MODEL 2: BOOK (with ForeignKey)
# =====================================
class Book(models.Model):
    """
    Represents a book written by an author.
    Uses ForeignKey to create a one-to-many relationship with Author.
    """
    title = models.CharField(max_length=200)
    
    # FOREIGNKEY EXPLANATION:
    # - Author: The model this book is linked to
    # - on_delete=models.CASCADE: If author is deleted, delete their books too
    # - related_name='books': Allows us to do author.books.all() to get all books by that author
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books'
    )
    
    def __str__(self):
        return self.title


# =====================================
# MODEL 3: LIBRARY (with ManyToMany)
# =====================================
class Library(models.Model):
    """
    Represents a library that contains many books.
    Uses ManyToManyField because:
    - One library can have many books
    - One book can be in many libraries
    """
    name = models.CharField(max_length=200)
    
    # MANYTOMANYFIELD EXPLANATION:
    # - Book: The model this library is linked to
    # - related_name='libraries': Allows us to do book.libraries.all() to see which libraries have this book
    books = models.ManyToManyField(
        Book, 
        related_name='libraries'
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        # This makes it say "Libraries" instead of "Librarys" in admin
        verbose_name_plural = "Libraries"


# =====================================
# MODEL 4: LIBRARIAN (with OneToOne)
# =====================================
class Librarian(models.Model):
    """
    Represents a librarian who manages exactly one library.
    Uses OneToOneField because:
    - One librarian manages one library
    - One library has one librarian
    """
    name = models.CharField(max_length=200)
    
    # ONETOONEFIELD EXPLANATION:
    # - Library: The model this librarian is linked to
    # - on_delete=models.CASCADE: If library is deleted, delete the librarian too
    # - related_name='librarian': Allows us to do library.librarian to get the librarian
    library = models.OneToOneField(
        Library, 
        on_delete=models.CASCADE, 
        related_name='librarian'
    )
    
    def __str__(self):
        return f"{self.name} - {self.library.name}"