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

