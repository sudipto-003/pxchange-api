from django.contrib import admin
from .models import C_User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Register your models here.
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'is_active', 'verified')
    list_filter = ('is_active', )
    fieldsets = (
        (None, {'fields': ('email', 'username')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'verified')}),
    )

    search_fields = ('email', )
    ordering = ('email', )
    filter_horizontal = ()


admin.site.register(C_User, UserAdmin)
admin.site.unregister(Group)