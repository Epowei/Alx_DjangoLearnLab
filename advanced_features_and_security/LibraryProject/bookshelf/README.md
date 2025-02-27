# Permissions and Groups in Django `relationship_app`

This document explains how permissions and groups are configured and utilized in the `relationship_app` of the `advanced_features_and_security` Django project to control access to various actions, enhancing security and functionality.

## Overview

The `relationship_app` uses Django's built-in permissions and groups system to manage access control for the `Book` model. Custom permissions are defined in the model, groups are created with specific permission sets, and views enforce these permissions using decorators.

## Step 1: Custom Permissions in Models

Custom permissions are defined in the `Book` model (`relationship_app/models.py`) within a `Meta` class. These permissions control specific actions on `Book` instances:

- **`can_view`**: Allows viewing the list of books.
- **`can_create`**: Allows creating new books.
- **`can_edit`**: Allows editing existing books.
- **`can_delete`**: Allows deleting books.

### Code Snippet
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication_year = models.IntegerField(default=2023)

    class Meta:
        permissions = (
            ('can_view', 'Can view book'),
            ('can_create', 'Can create book'),
            ('can_edit', 'Can edit book'),
            ('can_delete', 'Can delete book'),
            # Existing permissions retained
            ('can_add_book', 'Can add book'),
            ('can_change_book', 'Can change book'),
            ('can_delete_book', 'Can delete book'),
        )
```

### These permissions control different operations on book objects:

* can_view: Controls who can see detailed book information
* can_create: Controls who can add new books to the library
* can_edit: Controls who can modify existing book information
* can_delete: Controls who can remove books from the library

### Groups Configuration
The system uses Django's user groups to assign permissions to users based on their roles. Three main groups are defined:

1. Viewers: Users who can only view books but cannot modify them
2. Editors: Users who can view, add, and edit books
3. Admins: Users who have full access to all book operations, including deletion

### Setting Up Groups
To set up these groups, run the custom management command:
```
python manage.py setup_groups
```

This command creates the three groups and assigns appropriate permissions to each:

* Viewers: Assigned the can_view permission
* Editors: Assigned the can_view, can_create, and can_edit permissions
* Admins: Assigned all permissions (can_view, can_create, can_edit, can_delete)

Permission Enforcement
Permissions are enforced at multiple levels:

1. View-level Enforcement
The bookshelf/views.py file uses Django's permission_required decorator to restrict access to views:

```
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    # View implementation...
```

Similar decorators are used for create, edit, and delete views, ensuring that only users with the right permissions can access these functions.

2. Template-level Enforcement
Templates use conditional rendering to show or hide UI elements based on user permissions:
```
{% if perms.bookshelf.can_create %}
    <a href="{% url 'book_create' %}" class="btn btn-primary">Add New Book</a>
{% endif %}
```

This ensures that users only see options they have permission to use.

Admin Interface
The admin interface is configured in bookshelf/admin.py to provide administrators with tools to manage users, groups, and permissions:

Custom GroupAdmin enhances the group administration interface
Permission assignments can be managed through the admin interface

### Custom User Model
The system uses a custom user model (CustomUser) that extends Django's AbstractUser:
```
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
```

This custom user model is integrated with the permissions system to provide a complete user management solution.

How to Use the Permissions System
Assigning Users to Groups
Log in as an administrator
Navigate to the admin interface at /admin/
Select "Users" under the "Authentication and Authorization" section
Select a user to edit
Assign the user to one or more groups under the "Groups" field
Save changes
Testing Permission Access
Log in as a user from a specific group
Attempt to access different parts of the application
Verify that you can only access features permitted for your group
Adding Custom Permissions
To add additional permissions:

Define the new permission in the Meta class of the relevant model
Run migrations to update the database schema
Assign the new permission to appropriate groups
Update views and templates to enforce and respect the new permission
Best Practices
Always use the permission_required decorator for views that need protection
Check permissions in templates to hide UI elements users can't access
Use groups for role-based access control rather than assigning permissions directly to users
Review and audit permissions regularly to ensure they align with business requirements
Troubleshooting
If permissions aren't working as expected:

Check that migrations have been applied (python [manage.py](http://_vscodecontentref_/1) migrate)
Verify that the user is assigned to the correct group
Confirm that the group has the necessary permissions
Ensure that views are properly decorated with permission_required
Check that templates correctly use the perms context variable
