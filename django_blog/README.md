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


<br>
<br>


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

<br>
<br>


# Comment System Implementation

The comment system allows users to:

1. View all comments on a blog post
2. Add new comments if they're logged in
3. Edit their own comments
4. Delete their own comments

## Usage Instructions
### Viewing Comments
All visitors can view comments on any blog post by visiting the post's detail page.

### Adding Comments

* Logged-in users can add comments using the comment form at the bottom of a post.
* Non-logged-in users will see a prompt to log in to comment.

### Editing Comments
* Users can edit their own comments by clicking the "Edit" link next to their comment.
* The edit link only appears for comments the user authored.

### Deleting Comments
* Users can delete their own comments by clicking the "Delete" link next to their comment.
* A confirmation page will be shown before the comment is deleted.

### Permissions
* Viewing: Anyone can view comments.
* Creating: Only authenticated users can create comments.
* Editing: Users can only edit their own comments.
* Deleting: Users can only delete their own comments.

This implementation provides a complete comment system that integrates seamlessly with your existing blog application, following Django best practices with proper permission handling and user experience considerations.
