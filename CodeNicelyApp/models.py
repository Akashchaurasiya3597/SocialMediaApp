from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.contrib.auth.models import PermissionsMixin


# Create your models here.


class UserManager(BaseUserManager):
    def _create_user(self, phone_number, password,
                     is_staff, is_superuser, **extra_fields):
        user = self.model(phone_number=phone_number,

                          is_staff=is_staff,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        return self._create_user(phone_number, password, False, False,
                                 **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        return self._create_user(phone_number, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(
        max_length=255, unique=False, default=None, null=True, blank=True
    )
    email = models.EmailField(max_length=1000, blank=True, null=True, default=None)
    phone_number = models.CharField(max_length=10, unique=True, default=None)
    password = models.CharField(max_length=255, blank=False)

    created_date = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(
        'staff status', default=True,
        help_text='Designates whether the user can log into this admin site.'
    )
    is_superuser = models.BooleanField(
        'superuser status', default=True,
        help_text='Designates whether the user can log into this admin site.'
    )
    is_admin = models.BooleanField(
        default=False,

    )

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.phone_number


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    image = models.ImageField(blank=True, null=True, upload_to='post_pics')
    caption = models.CharField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='profile_pics')
    address = models.CharField(max_length=500)
    cover_photos = models.ImageField(upload_to='cover_pics')

    def __str__(self):
        return f'{self.user.full_name} Profile'


class Friend(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')  # who sent the request
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')  # who will receive the request
    status = models.CharField(max_length=20, default='connected')
    created_at = models.DateTimeField(auto_now_add=True)
