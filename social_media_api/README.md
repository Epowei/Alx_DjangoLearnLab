# Social Media API

## Setup Process
1. Install requirements: `pip install django djangorestframework`
2. Run migrations: `python manage.py makemigrations && python manage.py migrate`
3. Start server: `python manage.py runserver`

## User Registration
- Endpoint: POST `/api/register/`
- Body: {"username": "", "email": "", "password": "", "bio": "", "profile_picture": ""}
- Returns: Token

## User Authentication
- Endpoint: POST `/api/login/`
- Body: {"username": "", "password": ""}
- Returns: Token

## User Model
- Fields: username, email, bio, profile_picture, followers (ManyToMany)
- CustomUser extends AbstractUser

## Testing
Use Postman or curl to test endpoints. Include token in Authorization header for protected routes.

<br>

## API Endpoints Documentation

### Posts
1. __List all posts__

    * URL: GET /api/posts/
    * Query Parameters:
        * search: Search in title and content
        * page: Page number for pagination
        * page_size: Number of posts per page (max 100)

    * Authentication: Optional

2. __Create a post__

    * URL: POST /api/posts/
    * Body:
```
{
  "title": "My First Post",
  "content": "This is the content of my post."
}
```


* Authentication: Required

3. __Get post details__
    * URL: GET /api/posts/{post_id}/
    * Authentication: Optional

4. Update post
    * URL: PUT /api/posts/{post_id}/
    * Body:
```
{
  "title": "Updated Title",
  "content": "Updated content."
}
```
* Authentication: Required (must be author)

5. __Delete post__
    * URL: DELETE /api/posts/{post_id}/
    * Authentication: Required (must be author)

### Comments

1. List all comments
    * URL: GET /api/comments/
    * Query Parameters:
        * post: Filter by post ID
        * author: Filter by author ID
        * page: Page number for pagination
    * Authentication: Optional
2. Create a comment

    * URL: POST /api/comments/
    * Body:
```json
 {
 "content": "Updated comment content."
 }
```
   * Authentication:Required 
3. Get comment details
    * URL: GET /api/comments/{comment_id}/
    * Authentication: Optional

4. Update comment
    * URL: PUT /api/comments/{comment_id}/
    * Body
   ```json
    {
      "content": "Updated comment content."
    }
   ```
    * Authentication: Required (must be author)

5. Delete comment
    * URL: DELETE /api/comments/{comment_id}/
    * Authentication: Required (must be author)

<br>

### Testing with Postman

1. Create a Post:
    * Method: POST
    * URL: http://127.0.0.1:8000/api/posts/
    * Headers: Authorization: Token your_token_here
    * Body (JSON):
    
 ```json
    {
     "title": "My First Post",
     "content": "Hello world! This is my first post on the social media API."
    }
```
2. List Posts:
    * Method: GET
    * URL: http://127.0.0.1:8000/api/posts/
    * Optional Query Params: `? search=keyword&page=1 page_size=10`

3. Comment on a Post:
    * Method: POST
    * URL: `http://127.0.0.1:8000/api/comments/`
    * Headers: `Authorization: Token your_token_here`
    * Body (JSON):
    ```json
    {
    "post": 1,
    "content": "Great post! Thanks for sharing."
    }
    ```

<br>

## API Documentation For User Follows and Feed Functionality

**Follow Management**

1. Follow User

    * URL: POST /api/follow/{user_id}/
    * Description: Follow a user with the given ID
    * Authentication: Required
    * Response:
        * 200 OK - Successfully followed user
        * 400 Bad Request - Already following or trying to follow yourself

2. Unfollow User

    * URL: POST /api/unfollow/{user_id}/
    * Description: Unfollow a user you're currently following
    * Authentication: Required
    * Response:
        * 200 OK - Successfully unfollowed user
        * 400 Bad Request - Not following the user

3. Get Followers

    * URL: GET /api/followers/
    * Description: List all users who follow you
    * Authentication: Required
    * Response: Array of user objects
4. Get Following

    * URL: GET /api/following/
    * Description: List all users you follow
    * Authentication: Required
    * Response: Array of user objects

__Feed__
1. View Feed
    * URL: GET /api/feed/
    * Description: Get posts from users you follow, newest first
    * Authentication: Required
    * Query Parameters:
        * page: Page number (default: 1)
        * page_size: Number of posts per page (default: 10, max: 100)
    * Response: Paginated list of post objects


<br>

## API Documentation For Notifications and Likes Functionality

### Like System
1. Like a Post
    * URL: `POST /api/posts/{post_id}/like/`
    * Description: Like a specific post
    * Authentication: Required
    * Response:
        * Success (201): `{"success": "You liked the post 'Post Title'"}`
        * Error (400): `{"error": "You have already liked this post."}`
2. Unlike a Post

    * URL: `POST /api/posts/{post_id}/unlike/`
    * Description: Remove a like from a post
    * Authentication: Required
    * Response:
        * Success (200): `{"success": "You unliked the post 'Post Title'"}`
        * Error (400): `{"error": "You have not liked this post."}`

### Notification System
1. View Notifications

    * URL: `GET /api/notifications/`
    * Description: List all notifications for the current user
    * Authentication: Required
    * Response: Array of notification objects with recipient, actor, verb, timestamp, etc.

2. Mark Notification as Read

    * URL: `POST /api/notifications/{notification_id}/read/`
    * Description: Mark a specific notification as read
    * Authentication: Required
    * Response:
        * Success (200): `{"success": "Notification marked as read"}`
       * Error (404): `{"error": "Notification not found"}`

3. Mark All Notifications as Read

    * URL: `POST /api/notifications/read-all/`
    * Description: Mark all notifications as read
    * Authentication: Required
    * Response: `{"success": "All notifications marked as read"}`


### Testing

**Test Like Functionality**

Using Postman:

1. Login to get an authentication token
2. Create a post or use an existing one
3. Like the post:
    * POST to `/api/posts/1/like/` with Authentication header
4. Verify with GET to `/api/posts/1/` that is_liked is now true
5. Try liking again to check the duplicate prevention
6. Unlike the post:
    * POST to `/api/posts/1/unlike/` with Authentication header


### Test Notification Functionality
1. Create notifications through actions:
    * Like someone else's post
    * Comment on someone else's post
    * Follow another user
2. Check notifications:
    * GET to `/api/notifications/` to see all your notifications
3. Mark as read:
* POST to `/api/notifications/1/read/` to mark one as read
* POST to `/api/notifications/read-all/` to mark all as read

This implementation provides a comprehensive likes and notifications system for the social media API, enhancing user engagement and interactivity.

