from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, nickname, name, gender, age, username, password=None, **extra_fields):
        if not username:
            raise ValueError('O nome de usuário deve ser fornecido')
        user = self.model(
            nickname=nickname,
            name=name,
            gender=gender,
            age=age,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_admin(self, nickname, username, password=None, **extra_fields):
        if not username:
            raise ValueError('O nome de usuário deve ser fornecido')
        admin = self.model(
            nickname=nickname,
            username=username,
            **extra_fields
        )
        admin.password = make_password(password)  # Hash da senha
        admin.is_staff = True
        admin.is_admin = True
        admin.is_superuser = False
        admin.save(using=self._db)
        return admin
    
   
class User(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')
    gender = models.CharField(max_length=100, default='')
    age = models.PositiveIntegerField(null=True, blank=True)
    username = models.CharField(max_length=100, unique=True, default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    can_view_sidebar = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname', 'name']
    
    objects = UserManager()

    def __str__(self):
        return f'nickname: {self.nickname} | name: {self.name}'