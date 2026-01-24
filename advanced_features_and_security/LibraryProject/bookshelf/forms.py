from django import forms
from .models import Book

# Form to create or edit a book
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn']

# Form to search books by author
class BookSearchForm(forms.Form):
    author = forms.CharField(max_length=100, required=False)
    title = forms.CharField(max_length=100, required=False)
