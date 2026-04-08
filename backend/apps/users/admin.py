from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'phone', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'gender']
    search_fields = ['username', 'email', 'phone']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('其他信息', {'fields': ('phone', 'avatar', 'gender', 'birthday', 'address', 'balance')}),
    )
