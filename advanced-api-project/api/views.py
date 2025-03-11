from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework
from .models import Book
from .serializers import BookSerializer

# List all books with filtering, searching, and ordering
class BookListView(generics.ListAPIView):
    """
    GET: Retrieve a list of all books with advanced query capabilities.
    - Filtering: Filter by title, author, and publication_year (e.g., ?title=Book&author=1&publication_year=2020).
    - Searching: Search by title and author name (e.g., ?search=Jane).
    - Ordering: Order by title or publication_year (e.g., ?ordering=title or ?ordering=-publication_year).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view the list

    # Add filtering, searching, and ordering backends
    filter_backends = [filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Define fields for filtering
    filterset_fields = ['title', 'author', 'publication_year']
    
    # Define fields for searching
    search_fields = ['title', 'author__name']  # Search in book's title and author's name
    
    # Define fields for ordering
    ordering_fields = ['title', 'publication_year']
    
    # Default ordering (optional)
    ordering = ['title']  # Default sort by title ascending if no ordering specified

    def get_queryset(self):
        """
        Customize queryset to filter books by author ID if provided in query params (e.g., ?author=1).
        This works in addition to the filterset_fields.
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