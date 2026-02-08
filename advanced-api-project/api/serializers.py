from rest_framework import serializers
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model"""
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        read_only_fields = ['id']
    
    def validate_publication_year(self, value):
        """Validate that publication year is reasonable"""
        if value < 1000 or value > 2100:
            raise serializers.ValidationError("Publication year must be between 1000 and 2100.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for the Author model"""
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'date_of_birth', 'books']
        read_only_fields = ['id']
    
    def validate_name(self, value):
        """Validate that author name is not empty"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("Author name cannot be empty.")
        return value