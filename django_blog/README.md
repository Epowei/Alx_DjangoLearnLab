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

