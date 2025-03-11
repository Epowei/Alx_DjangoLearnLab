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