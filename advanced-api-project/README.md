# Advanced API Project

A Django REST Framework project demonstrating CRUD operations for a Book API with nested Author relationships.

## Project Structure
- `advanced_api_project/`: Main project directory.
- `api/`: App containing models, serializers, views, and URLs.

## API Endpoints
- **GET /api/books/**: List all books, optionally filtered by `?author=<id>`.
- **POST /api/books/**: Create a new book (authenticated users only).
- **GET /api/books/<id>/**: Retrieve a specific book.
- **PUT /api/books/<id>/**: Update a specific book (authenticated users only).
- **DELETE /api/books/<id>/**: Delete a specific book (authenticated users only).

## View Configurations
- **BookListCreateView**:
  - Uses `ListCreateAPIView` for GET and POST.
  - Custom `get_queryset` filters books by author ID if provided.
  - Permissions: Read-only for unauthenticated; full access for authenticated.
- **BookDetailView**:
  - Uses `RetrieveUpdateDestroyAPIView` for GET, PUT, DELETE.
  - Permissions: Read-only for unauthenticated; full access for authenticated.

## Custom Settings
- **Serializer Validation**: Ensures `publication_year` is not in the future.
- **Permissions**: `IsAuthenticatedOrReadOnly` restricts write operations to authenticated users.

## Running the Project
1. Activate virtual environment: `source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver`

## Testing
Use tools like Postman or curl to test endpoints. Ensure authentication (e.g., Basic Auth) for write operations.

## Testing Strategy
Unit tests are implemented in `api/test_views.py` to ensure API endpoints function correctly.

### Test Coverage
- **CRUD Operations**: Tests for listing, retrieving, creating, updating, and deleting books.
- **Query Features**: Tests for filtering (by title, author, publication_year), searching (title, author name), and ordering (title, publication_year).
- **Permissions**: Tests to verify unauthenticated users can only read, while authenticated users can write.

### Key Test Cases
1. **List Books**: Verifies all books are returned with correct data.
2. **Filtering**: Checks filtering by title works (e.g., `?title=Pride`).
3. **Searching**: Ensures search by author name returns expected results (e.g., `?search=Jane`).
4. **Ordering**: Confirms ordering by publication year works (e.g., `?ordering=-publication_year`).
5. **Create/Update/Delete**: Tests authenticated success and unauthenticated failure scenarios.

### Running Tests
Run the test suite:
```bash
python manage.py test api