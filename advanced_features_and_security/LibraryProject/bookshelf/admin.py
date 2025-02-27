from django.contrib import admin
from .models import Book, CustomUser, Author, Library, Librarian, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission

class BookAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('title', 'author', 'publication_year')

    # Add filters for author and publication year
    list_filter = ('author', 'publication_year')

    # Enable search by title and author
    search_fields = ('title', 'author')

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'date_of_birth', 'role', 'get_groups']
    list_filter = ['date_of_birth', 'groups']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'date_of_birth', 'profile_photo'),
        }),
    )

    def role(self, obj):
        return obj.userprofile.role if hasattr(obj, 'userprofile') else 'N/A'
    role.short_description = 'Role'

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()]) if obj.groups.exists() else "-"
    get_groups.short_description = 'Groups'

# Register models
admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Author)
admin.site.register(Library)
admin.site.register(Librarian)
admin.site.register(UserProfile)

# Make sure Group and Permission are registered (they should be by default)
# Re-register them with better search fields
admin.site.unregister(Group)

class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_permissions']
    search_fields = ['name']
    filter_horizontal = ['permissions']

    def get_permissions(self, obj):
        return ", ".join([p.name for p in obj.permissions.all()[:5]]) + ("..." if obj.permissions.count() > 5 else "")
    get_permissions.short_description = 'Permissions'

admin.site.register(Group, GroupAdmin)