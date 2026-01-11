# Delete Book Examples

```python
from bookshelf.models import Book

# Delete a specific book by title
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Delete using filter
Book.objects.filter(title="Nineteen Eighty-Four").delete()

# Delete all books by an author
Book.objects.filter(author="George Orwell").delete()

# Delete all books (use with caution!)
Book.objects.all().delete()
```
