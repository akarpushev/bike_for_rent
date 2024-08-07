# bikes/serializers.py

from rest_framework import serializers
from .models import Bike, Rent
from django.utils import timezone


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ['id', 'bike', 'status']  # Определяет, какие поля модели будут включены в сериализованный JSON.


# class RentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Rent
#         # fields = ('user', 'bike', 'start_time') # можно [] или ()
#         fields = ['bike', 'start_time']  # можно [] или ()
#
#     def create(self, validated_data):
#         user = validated_data['user']
#         bike = validated_data['bike']
#
#         # Проверка, есть ли уже аренда для пользователя
#         if Rent.objects.filter(user=user).exists():
#             raise serializers.ValidationError("User already has a rented bike.")
#
#         # Проверка доступности велосипеда
#         if bike.status != 'available':
#             raise serializers.ValidationError("Bike is not available for rent.")
#
#         # Обновление статуса велосипеда
#         bike.status = 'rented'
#         bike.save()
#
#         # Создание новой записи аренды
#         rent = Rent.objects.create(user=user, bike=bike)
#         return rent


class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = ['bike', 'start_time']

    # можно убрать
    # def create(self, validated_data):
    #     # Удалите проверки из сериализатора
    #     return super().create(validated_data)


class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = ['end_time']

    def update(self, instance, validated_data):
        # Метод update принимает два аргумента: instance (существующий объект модели, который нужно обновить)
        # и validated_data (данные, прошедшие валидацию).
        instance.end_time = validated_data.get('end_time', timezone.now())
        instance.cost = instance.calculate_cost()
        instance.bike.status = 'available'
        instance.bike.save()  # сохраняет изменения в объекте bike в базу данных.
        instance.save()  # сохраняет изменения в объекте rent (инстансе) в базу данных
        return instance
    # instance - это объект модели Rent, который уже существует в бд и представляет строку в таблице bikes_rent
    # Django Rest Framework (DRF) вызывает метод update внутри UpdateAPIView при обработке HTTP PUT или PATCH запроса.
    #
    # Когда вызывается метод put или patch в UpdateAPIView, в class ReturnBikeView(generics.UpdateAPIView):
    # он автоматически передает объект модели (instance)
    # и валидированные данные (validated_data) в метод update сериализатора.
    # Это происходит внутри методов perform_update и update самого UpdateAPIView.
