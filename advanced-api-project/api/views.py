from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# List all books
class BookListView(generics.ListAPIView):
    """
    GET: Retrieve a list of all books, optionally filtered by author ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view the list

    def get_queryset(self):
        """
        Customize queryset to filter books by author ID if provided in query params (e.g., ?author=1).
        """
        queryset = Book.objects.all()
        author_id = self.request.query_params.get('author', None)
        if author_id is not None:
            queryset = queryset.filter(author_id=author_id)
        return queryset

# Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve details of a specific book by its ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view details

# Create a new book
class BookCreateView(generics.CreateAPIView):
    """
    POST: Create a new book instance.
    Only authenticated users can create books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can create

    def perform_create(self, serializer):
        """
        Hook to handle additional logic during creation.
        """
        serializer.save()

# Update an existing book
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update an existing book by ID.
    Only authenticated users can update books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can update

    def perform_update(self, serializer):
        """
        Hook to handle additional logic during update.
        """
        serializer.save()

# Delete a book
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Remove a book from the database.
    Only authenticated users can delete books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can delete