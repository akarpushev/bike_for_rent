# users/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    # Определение класса сериализатора для модели User
    password = serializers.CharField(write_only=True)
    # Поле для пароля, доступное только для записи (не отображается при чтении данных)

    class Meta:
        # Вложенный класс Meta для настройки поведения сериализатора
        model = User
        # Указывает, что сериализатор работает с моделью User
        fields = ('email', 'username', 'password')
        # Определяет, какие поля модели будут включены в сериализацию и десериализацию

    def create(self, validated_data):
        # Метод для создания нового объекта User
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        # Создание нового пользователя с указанными email и username
        user.set_password(validated_data['password'])
        # set_password() встроен в Django и автоматически хэширует пароль
        # Установка зашифрованного пароля для пользователя
        user.save()
        # Сохранение пользователя в базе данных
        return user
        # Возвращает созданного пользователя


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
