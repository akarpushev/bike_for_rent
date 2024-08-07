# bikes/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Bike(models.Model):
    # models.Model - таблица в бд
    # с полями name, status

    # STATUS_CHOICES = [
    #     ('available', 'Available'),
    #     ('rented', 'Rented'),
    # ]

    bike = models.CharField(max_length=100)  # Название велосипеда
    # status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')  # Статус велосипеда
    status = models.CharField(max_length=50, choices=[('available', 'Available'), ('rented', 'Rented')])

    # is_available = models.BooleanField(default=True)

    # def save(self, *args, **kwargs):
    #     if not self.is_available:
    #         raise ValidationError("Bike is not available for rent.")
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.bike


class Rent(models.Model):
    # наследуется от models.Model.
    # Это означает, что Rent является моделью Django и будет сохранен в базе данных как таблица.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Поле user создается как одно-ко-одному связь с моделью User (пользователь).
    # Каждый арендованный велосипед связан с одним конкретным пользователем,
    # и один пользователь может арендовать только один велосипед одновременно.

    # on_delete=models.CASCADE
    # Если пользователь будет удален, то все связанные с ним записи аренды также будут удалены.

    bike = models.OneToOneField(Bike, on_delete=models.CASCADE)
    # Поле bike создается как одно-ко-одному связь с моделью Bike (велосипед).
    # Это означает, что каждый арендованный велосипед связан с одной конкретной записью аренды,
    # и каждый велосипед может быть арендован только один раз за раз.

    # on_delete=models.CASCADE
    # Если велосипед будет удален, то все связанные с ним записи аренды также будут удалены.

    start_time = models.DateTimeField(auto_now_add=True)
    # Поле start_time является DateTimeField (поле даты и времени).
    # auto_now_add=True
    # Значение этого поля будет автоматически установлено на текущие дату и время в момент создания записи.

    # Для реализации API возврата велосипеда и расчета стоимости аренды
    end_time = models.DateTimeField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def __str__(self):
        return f"{self.user.username} rented {self.bike.bike} from {self.start_time} to {self.end_time}"
        # return f"{self.user.username} rented {self.bike.bike} at {self.start_time}"

    @property
    def status(self):
        return self.bike.status

    def calculate_cost(self):
        if self.end_time and self.start_time:
            duration = self.end_time - self.start_time
            # Пример расчета стоимости: 1.00 единица за минуту
            return duration.total_seconds() / 60 * 1.00
        return 0
