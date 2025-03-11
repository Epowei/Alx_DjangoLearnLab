from rest_framework import serializers
from .models import Author, Book
from django.utils import timezone

# Serializer for Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']  # Include all fields
    
    # Custom validation for publication_year
    def validate_publication_year(self, value):
        """
        Ensure the publication year is not in the future.
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year {value} cannot be in the future (current year: {current_year})."
            )
        return value

# Serializer for Author model with nested books
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer to include all books by this author
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']  # Include name and related books
    
    """
    The 'books' field uses a nested BookSerializer to dynamically serialize
    all books associated with the author through the ForeignKey relationship.
    The 'many=True' argument indicates this is a one-to-many relationship,
    and 'read_only=True' prevents books from being modified through this serializer.
    """