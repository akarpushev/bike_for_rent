# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Модель пользователя в базе данных
    """
    email = models.EmailField(unique=True, null=True, blank=True)

    USERNAME_FIELD = 'username'
    # Это определяет, что для аутентификации пользователей будет использоваться поле username.
    REQUIRED_FIELDS = []
    # Это список полей обязательных для заполнения при создании суперпользователя через команду createsuperuser.
    # Список пуст, что означает, что никаких дополнительных полей (кроме USERNAME_FIELD и пароля) не требуется.

    def __str__(self):
        return self.username  # в админке, будет отображаться username пользователя.
