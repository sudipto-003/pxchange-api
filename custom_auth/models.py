from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken


class C_Manager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)

        user.is_admin = True
        user.verified = True
        user.is_active = True
        user.save()

        return user


class C_User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email Address', max_length=255, unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    auth_provider = models.CharField(max_length=50, default='email')
    joined = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = C_Manager()

    def __str__(self):
        return self.email

    def is_verified(self):
        return self.verified

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin