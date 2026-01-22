from relationship_app.models import Author, Book, Library, Librarian

# Query 1: Get all books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    for book in books:
        print(f"Book Title: {book.title}, Author: {book.author.name}")

# Query 2: List all books in a specific library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    for book in books:
        print(f"Book Title: {book.title}")

# Query 3: Retrieve the librarian for a specific library
def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    librarian = Librarian.objects.get(library=library)
    print(f"Librarian for {library.name}: {librarian.name}")

# Sample queries
if __name__ == "__main__":
    print("Books by Author 'J.K. Rowling':")
    books_by_author('J.K. Rowling')

    print("\nBooks in 'City Library':")
    books_in_library('City Library')

    print("\nLibrarian for 'Central Library':")
    librarian_for_library('Central Library')
