from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True
    )
    username = models.CharField(
        'Юзернейм',
        max_length=150,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150
    )
    password = models.CharField(
        'Пароль',
        max_length=150
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

