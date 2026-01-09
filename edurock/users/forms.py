from django.contrib.auth import forms as admin_forms
from django.forms import EmailField, ImageField
from allauth.account.forms import SignupForm
from django.utils.translation import gettext_lazy as _
from .models import User

class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        field_classes = {"email": EmailField}

class UserAdminCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }

class UserSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        return user