from rest_framework import serializers
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model"""
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'description', 'price']
        read_only_fields = ['id']


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for the Author model"""
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'date_of_birth', 'books']
        read_only_fields = ['id']