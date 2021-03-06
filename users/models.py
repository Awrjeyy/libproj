from asyncio.windows_events import NULL
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _ 
from django.conf import settings
from django.db.models.signals import post_save
from PIL import Image
from .managers import CustomUserManager
# Create your models here.

User = settings.AUTH_USER_MODEL

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    bio = models.TextField(default=NULL)
    user_img = models.ImageField(default='default.jpg',
        upload_to='profile-pics',
    )
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.user_img.path)

        if img.height > 100 or img.width > 100:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.user_img.path)
