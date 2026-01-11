# Update Book Examples

```python
# Update a book's title
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Alternative method using update()
Book.objects.filter(title="1984").update(title="Nineteen Eighty-Four")
```
