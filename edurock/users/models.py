from typing import ClassVar
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .managers import UserManager

class User(AbstractUser):
    name = CharField(_("Name of User"), blank=True, max_length=255)
    image = models.ImageField(_("Profile Image"), upload_to="users/", blank=True, null=True)
    
    first_name = None
    last_name = None
    email = EmailField(_("email address"), unique=True)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.id})
class AboutUs(models.Model):
    title = models.CharField(_("Admin Page Title"), max_length=255, default="About Us Page")
    updated_at = models.DateTimeField(auto_now=True)
    quote_text = models.TextField(_("Philosophy Quote"), blank=True, null=True)
    
    card_01_title = models.CharField(_("Card 01 Title"), max_length=255, default="Why Book Buddy Exists")
    card_01_text = models.TextField(_("Card 01 Content"), blank=True, null=True)
    
    card_02_title = models.CharField(_("Card 02 Title"), max_length=255, default="Why Families Choose Us")
    card_02_list = models.TextField(_("Card 02 List Items"), help_text="Enter one item per line", blank=True, null=True)
    
    card_03_title = models.CharField(_("Card 03 Title"), max_length=255, default="What Makes Us Different")
    card_03_list = models.TextField(_("Card 03 List Items"), help_text="Enter one item per line", blank=True, null=True)
    
    card_04_title = models.CharField(_("Card 04 Title"), max_length=255, default="How We Grow Together")
    card_04_text = models.TextField(_("Card 04 Content"), blank=True, null=True)
class StudentActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    page_visited = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Student Activity")
        verbose_name_plural = _("Student Activities")