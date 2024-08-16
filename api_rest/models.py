from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_superuser(self, nickname, name,age, username, password=None,id_user=None , **extra_fields):
        if not username:
            raise ValueError('O nome de usuário deve ser fornecido')
        superuser = self.model(
            nickname=nickname,
            name=name,
            age=age,
            username=username,
            id_user=id_user,
            **extra_fields
        )
        superuser.set_password(password)
        superuser.save(using=self._db)
        return superuser
    
    def create_admin(self, nickname, username, password=None, id_user=None ,**extra_fields):
        if not username:
            raise ValueError('O nome de usuário deve ser fornecido')
        admin = self.model(
            nickname=nickname,
            username=username,
            id_user = id_user,
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
    id_user = models.CharField(max_length=100, default='')
    username = models.CharField(max_length=100, unique=True, default='')
    area = models.CharField(max_length=100, default='')
    age = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname', 'name']
    
    objects = UserManager()

    def __str__(self):
        return f'nickname: {self.nickname} | name: {self.name}'

class Relatorio(models.Model):
    data = models.CharField(max_length=100)
    horario = models.CharField(max_length=100)
    supervisores = models.TextField()

    def __str__(self):
        return f"Relatorio {self.data} - {self.horario}"
    
class CallStaff(models.Model):
    relatorio = models.ForeignKey(Relatorio, on_delete=models.CASCADE, related_name='callstaffs')
    call = models.CharField(max_length=100)
    staff = models.CharField(max_length=100)

