from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import requests
import logging

class UserManager(BaseUserManager):
    
    def create_user(self, nickname, area, age, username, password=None, id_user=None, **extra_fields):
        if not username:
            raise ValueError('O nome de usuário deve ser fornecido')
        user = self.model(
            nickname=nickname,
            id_user=id_user,
            area=area,
            age=age,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, username, password=None, **extra_fields):
        if not username:
            raise ValueError('O nome de usuário deve ser fornecido')
         
        nickname = nickname.strip()
        username = self.model.normalize_username(username.strip())

        superuser = self.model(
            nickname=nickname,
            username=username,
            **extra_fields
        )
        superuser.is_staff = True
        superuser.is_admin = True
        superuser.is_superuser = True
        superuser.set_password(password)
        superuser.save(using=self._db)
        return superuser
    
    def create_admin(self, nickname, username, password=None, id_user=None, **extra_fields):
        if not username:
            raise ValueError('O nome de usuário deve ser fornecido')

        admin = self.model(
            nickname=nickname,
            username=username,
            id_user=id_user,
            **extra_fields
        )
        admin.password = make_password(password)  # Hash da senha
        admin.is_staff = True
        admin.is_admin = True
        admin.is_superuser = False
        admin.save(using=self._db)
        return admin

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True, default='', blank=False)
    nickname = models.CharField(max_length=100, default='', blank=False)  
    id_user = models.CharField(max_length=100, default='', blank=False)   
    area = models.CharField(max_length=100, default='', blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname']

    objects = UserManager()

    def __str__(self):
        return f'Nickname: {self.nickname} | Username: {self.username}'

    def clean(self):
        super().clean()
        if self.age is not None and (self.age < 0 or self.age > 120):
            raise ValidationError({'age': 'A idade deve estar entre 0 e 120'})

        if self.id_user and len(self.id_user) != 18:
            raise ValidationError({'id_user': 'O ID do usuário deve ter exatamente 18 caracteres.'})

    def save(self, *args, **kwargs):
        self.username = self.username.strip()
        super().save(*args, **kwargs)
        return User

class Relatorio(models.Model):
    data = models.DateField(default=timezone.now)
    horario = models.TimeField(default=timezone.now)
    supervisores = models.TextField()

    def __str__(self):
        return f"Relatório {self.data} - {self.horario}"

class CallStaff(models.Model):
    relatorio = models.ForeignKey(Relatorio, on_delete=models.CASCADE, related_name='callstaffs')
    call = models.CharField(max_length=100)
    staff = models.CharField(max_length=100)

class CookieUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cookie_value = models.CharField(max_length=16) 
    created_at = models.DateTimeField(auto_now_add=True)

class DiscordServer(models.Model):
    guild_id = models.CharField(max_length=100, unique=True)
    member_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
