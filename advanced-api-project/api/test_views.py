from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Book, Author
from .serializers import BookSerializer

class BookAPITestCase(APITestCase):
    def setUp(self):
        """
        Set up initial data for all test cases.
        Creates an author and two books, plus a test user for authentication tests.
        """
        self.client = APIClient()
        
        # Create a test user
        self.user = self.client.post(
            reverse('admin:login'),
            {'username': 'testuser', 'password': 'testpass'}
        )
        self.client.login(username='testuser', password='testpass')  # Log in for authenticated tests
        
        # Create test data
        self.author = Author.objects.create(name="Jane Austen")
        self.book1 = Book.objects.create(
            title="Pride and Prejudice", publication_year=1813, author=self.author
        )
        self.book2 = Book.objects.create(
            title="Sense and Sensibility", publication_year=1811, author=self.author
        )
    
    def tearDown(self):
        """
        Clean up after each test (optional, as test DB is reset automatically).
        """
        self.client.logout()

    # Test BookListView (GET)
    def test_list_books(self):
        """Test retrieving the list of all books."""
        url = reverse('book-list')
        response = self.client.get(url)
        
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_books_by_title(self):
        """Test filtering books by title."""
        url = reverse('book-list') + '?title=Pride'
        response = self.client.get(url)
        
        books = Book.objects.filter(title__icontains="Pride")
        serializer = BookSerializer(books, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)

    def test_search_books_by_author_name(self):
        """Test searching books by author's name."""
        url = reverse('book-list') + '?search=Jane'
        response = self.client.get(url)
        
        books = Book.objects.filter(author__name__icontains="Jane")
        serializer = BookSerializer(books, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data, serializer.data)

    def test_order_books_by_publication_year(self):
        """Test ordering books by publication_year descending."""
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        
        books = Book.objects.order_by('-publication_year')
        serializer = BookSerializer(books, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # Test BookDetailView (GET)
    def test_retrieve_book(self):
        """Test retrieving a single book by ID."""
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        serializer = BookSerializer(self.book1)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # Test BookCreateView (POST)
    def test_create_book_authenticated(self):
        """Test creating a book as an authenticated user."""
        url = reverse('book-create')
        data = {
            "title": "Emma",
            "publication_year": 1815,
            "author": self.author.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(title="Emma").publication_year, 1815)

    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication fails."""
        self.client.logout()  # Log out to test unauthenticated access
        url = reverse('book-create')
        data = {
            "title": "Emma",
            "publication_year": 1815,
            "author": self.author.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2)  # No new book created

    # Test BookUpdateView (PUT)
    def test_update_book_authenticated(self):
        """Test updating a book as an authenticated user."""
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            "title": "Pride and Prejudice Updated",
            "publication_year": 1814,
            "author": self.author.pk
        }
        response = self.client.put(url, data, format='json')
        
        self.book1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.book1.title, "Pride and Prejudice Updated")
        self.assertEqual(self.book1.publication_year, 1814)

    def test_update_book_unauthenticated(self):
        """Test updating a book without authentication fails."""
        self.client.logout()
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            "title": "Pride and Prejudice Updated",
            "publication_year": 1814,
            "author": self.author.pk
        }
        response = self.client.put(url, data, format='json')
        
        self.book1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.book1.title, "Pride and Prejudice")  # No change

    # Test BookDeleteView (DELETE)
    def test_delete_book_authenticated(self):
        """Test deleting a book as an authenticated user."""
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book_unauthenticated(self):
        """Test deleting a book without authentication fails."""
        self.client.logout()
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2)  # Book not deleted