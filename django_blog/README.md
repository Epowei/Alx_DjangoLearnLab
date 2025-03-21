# Authentication System Overview
The authentication system provides:

* __Registration:__ Users can create accounts with a username, password, and optional email.

* __Login:__ Authenticated users access the site using Django’s LoginView.

* __Logout:__ Users can end their session with LogoutView.

* __Profile:__ Authenticated users can update their email (extendable to more fields).

### Setup Instructions
1. Ensure dependencies are installed: pip install django.

2. Apply migrations: python manage.py migrate.

3. Start the server: python manage.py runserver.

4. Access endpoints: /register, /login, /logout, /profile.

### User Guide
* Register: Visit /register, fill out the form, and submit.

* Login: Go to /login, enter credentials, and submit.

* Profile: After logging in, visit /profile to update your email.

* Logout: Click “Logout” from the navigation bar.





# Blog Post Management

## Features
- **List Posts**: View all blog posts on the homepage.
- **View Post Details**: Click on a post title to view its full content.
- **Create Post**: Authenticated users can create new posts.
- **Edit Post**: Authors can edit their own posts.
- **Delete Post**: Authors can delete their own posts.

## URLs
- `/`: List all posts.
- `/posts/new/`: Create a new post.
- `/posts/<int:pk>/`: View post details.
- `/posts/<int:pk>/edit/`: Edit a post.
- `/posts/<int:pk>/delete/`: Delete a post.

## Permissions
- Only authenticated users can create posts.
- Only the author of a post can edit or delete it.

## Testing
1. Start the server: `python manage.py runserver`.
2. Test all CRUD operations.
3. Verify permissions for editing and deleting posts.

