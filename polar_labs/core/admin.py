from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.base_admin import BaseAdmin
from core.models import PolarLabsUser


# Register out own model admin, based on the default UserAdmin
@admin.register(PolarLabsUser)
class CustomUserAdmin(BaseAdmin, UserAdmin):
	pass
