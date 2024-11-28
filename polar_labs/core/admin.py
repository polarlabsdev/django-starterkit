from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.base_admin import BaseAdmin
from core.models import CoreUser


# Register out own model admin, based on the default UserAdmin
@admin.register(CoreUser)
class CustomUserAdmin(BaseAdmin, UserAdmin):
	pass
