# users/views.py

from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer

User = get_user_model()


class RegisterUserView(generics.CreateAPIView):
    """
    Это класс-представление (view) Django REST Framework (DRF), который предоставляет API для создания новых объектов
     (в данном случае — пользователей).
    Отвечает за обработку HTTP-запросов для регистрации нового пользователя с помощью API
    """
    queryset = User.objects.all()  # переменная queryset будет содержать все объекты модели User
    permission_classes = (AllowAny,)  # Указывает, что для доступа к этому представлению не требуется аутентификация
    serializer_class = RegisterSerializer

    # Дополнительная логика не требуется, если просто создать нового пользователя по данным, отправленным в запросе.

    # Если нужна дополнительная логика перед созданием пользователя
    # def perform_create(self, serializer):
        # Добавить валидацию или обработку данных перед созданием пользователя.
        # Модифицировать процесс создания пользователя.
        # Выполнить какие-то действия после создания пользователя.
        # serializer.save()


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    #def post(self, request, *args, **kwargs):
    def post(self, request):
        serializer = self.get_serializer(data=request.data)  # Получаем сериализатор с данными из запроса
        # request.data — это данные, отправленные в теле запроса, например, JSON или форма.
        # data=request.data передает эти данные в сериализатор, чтобы сериализатор мог их обработать и проверить.
        serializer.is_valid(raise_exception=True)  # Проверяем, что данные валидны, и если нет, выбрасываем исключение

        # Извлекаем имя пользователя и пароль из проверенных данных
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            # Пытаемся найти пользователя по имени
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Если пользователь не найден, возвращаем ошибку с кодом 401 (Неавторизован)
            return Response({"error": "Invalid username or password"}, status=401)

        # user = User.objects.get(email=serializer.validated_data['email'])
        # if user.check_password(serializer.validated_data['password']):
        #     refresh = RefreshToken.for_user(user)
        #     return Response({
        #         'refresh': str(refresh),
        #         'access': str(refresh.access_token),
        #     })
        # return Response({"detail": "Invalid credentials"}, status=401)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid username or password"}, status=401)


def home(request):
    return HttpResponse("Welcome to the Bike Rent API!")
