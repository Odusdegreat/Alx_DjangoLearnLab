from django import forms
from .models import Book  # Assuming you have a Book model

# Example Form for the Book model (creating or editing a book)
class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn']  # List of fields you want to include

    # You can also add custom validations or field-specific logic here
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if len(isbn) != 13:
            raise forms.ValidationError("ISBN must be 13 characters long.")
        return isbn
