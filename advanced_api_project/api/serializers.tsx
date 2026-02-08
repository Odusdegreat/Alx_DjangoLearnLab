from django.utils import timezone
from rest_framework import serializers
from .models import Author, Book

# BookSerializer serializes all fields of the Book model.
# It also validates that publication_year is not in the future.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    # Custom validation for publication_year.
    def validate_publication_year(self, value: int) -> int:
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError("publication_year cannot be in the future.")
        return value


# AuthorSerializer serializes Author and includes nested Books.
# The 'books' field uses the Author -> Book relationship via related_name="books".
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
