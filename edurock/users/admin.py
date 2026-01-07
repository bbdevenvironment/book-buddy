from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import User
from .models import AboutUs

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "is_superuser"]
    search_fields = ["name"]
    ordering = ["id"]
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ["title", "card_01_title", "updated_at"]
    fieldsets = (
        (_("General Info"), {"fields": ("title", "quote_text")}),
        (_("Philosophy Card 01"), {"fields": ("card_01_title", "card_01_text")}),
        (_("Philosophy Card 02 (List)"), {"fields": ("card_02_title", "card_02_list")}),
        (_("Philosophy Card 03 (List)"), {"fields": ("card_03_title", "card_03_list")}),
        (_("Philosophy Card 04"), {"fields": ("card_04_title", "card_04_text")}),
    )

    def has_add_permission(self, request):
        if AboutUs.objects.exists():
            return False
        return True