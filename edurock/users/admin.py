from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _
from .models import User, AboutUs, StudentActivity
from .forms import UserAdminChangeForm, UserAdminCreationForm

admin.site.site_header = _("Book Buddy LMS Dashboard")

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (_("Login Credentials"), {"fields": ("email", "password")}),
        (_("Student Profile"), {"fields": ("name", "image")}),
        (_("Access Control"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("System Logs"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "is_staff"]
    search_fields = ["name", "email"]
    ordering = ["-date_joined"]

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ["title", "updated_at"]
    def has_add_permission(self, request):
        return not AboutUs.objects.exists()

@admin.register(StudentActivity)
class StudentActivityAdmin(admin.ModelAdmin):
    list_display = ["user", "page_visited", "timestamp"]
    readonly_fields = ["user", "page_visited", "timestamp"]
    list_filter = ["timestamp"]