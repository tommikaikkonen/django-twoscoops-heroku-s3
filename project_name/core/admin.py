from core.forms import UserCreationForm, UserChangeAdminForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User

class EmailUserAdmin(UserAdmin):
    form = UserChangeAdminForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_email_verified', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
 
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
 
    list_display = ('email', 'is_email_verified')
    list_filter = ('is_active', 'is_email_verified')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)

admin.site.register(User, EmailUserAdmin)