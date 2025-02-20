from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User, UserProfile

class CustomUserAdmin(UserAdmin):
    # admin panel里的用户表格里显示哪些字段
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
