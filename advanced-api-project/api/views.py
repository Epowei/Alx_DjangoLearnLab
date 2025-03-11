from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# List all books or create a new book
class BookListCreateView(generics.ListCreateAPIView):
    """
    GET: Retrieve a list of all books, optionally filtered by author ID.
    POST: Create a new book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Read-only for unauthenticated users

    def get_queryset(self):
        """
        Customize queryset to filter books by author ID if provided in query params (e.g., ?author=1).
        """
        queryset = Book.objects.all()
        author_id = self.request.query_params.get('author', None)
        if author_id is not None:
            queryset = queryset.filter(author_id=author_id)
        return queryset

    def perform_create(self, serializer):
        """
        Hook to handle additional logic during creation.
        Ensures the serializer's validation (e.g., publication_year) is applied before saving.
        """
        serializer.save()

# Retrieve, update, or delete a specific book
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single book by ID.
    PUT: Update an existing book.
    DELETE: Delete a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Read-only for unauthenticated users

    def perform_update(self, serializer):
        """
        Hook to handle additional logic during update.
        Ensures validation (e.g., publication_year not in future) is respected.
        """
        serializer.save()