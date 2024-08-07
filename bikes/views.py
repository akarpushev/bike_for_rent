# bikes/views.py

from .models import Bike, Rent
from .serializers import BikeSerializer
from .serializers import RentSerializer
from .serializers import ReturnSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status


class BikeListView(generics.ListAPIView):
    queryset = Bike.objects.filter(status='available')
    # Определяет, какие объекты будут возвращены.
    # В данном случае это велосипеды со статусом available.
    serializer_class = BikeSerializer
    # Указывает, какой сериализатор использовать для преобразования данных.


class RentBikeView(generics.CreateAPIView):
    # CreateAPIView обрабатывает HTTP POST запросы для создания новых объектов (в данном случае, аренды велосипеда).
    queryset = Rent.objects.all()
    # Определяет набор данных (queryset), с которым будет работать представление.
    # В данном случае, это все объекты модели Rent.
    permission_classes = [permissions.IsAuthenticated]
    # Определяет, что доступ к этому представлению имеют только аутентифицированные пользователи.
    serializer_class = RentSerializer

    def perform_create(self, serializer):
        user = self.request.user  # Получает текущего аутентифицированного пользователя, который делает запрос.
        bike = serializer.validated_data['bike']  # Получает велосипед из валидированных данных сериализатора.

        # # Проверяем доступность велосипеда
        # if not bike.is_available:
        #     raise ValidationError("Bike is not available for rent.")

        # Проверяет, существует ли уже аренда для текущего пользователя.
        if Rent.objects.filter(user=user).exists():
            raise ValidationError("User already has a rented bike.")
        if bike.status != 'available':  # Проверяет, доступен ли велосипед для аренды.
            raise ValidationError("Bike is not available for rent.")
        serializer.save(user=user, start_time=timezone.now())
        # Сохраняет объект аренды с указанием пользователя и текущего времени начала аренды.
        bike.status = 'rented'
        bike.save()


class ReturnBikeView(generics.UpdateAPIView):
    queryset = Rent.objects.all()
    serializer_class = ReturnSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Найдите аренду для текущего пользователя и текущего велосипеда
        user = self.request.user
        bike_id = self.kwargs.get('bike_id')
        return generics.get_object_or_404(Rent, user=user, bike_id=bike_id, end_time__isnull=True)

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()  # получает объект, который будет обновлен (instance).
        serializer = self.get_serializer(self.object, data=request.data, partial=True)
        # создает сериализатор с этим объектом и новыми данными.
        if serializer.is_valid():  # проверяет валидность данных.
            self.perform_update(serializer)  # self.perform_update(serializer), внутри вызывает serializer.save()
            # serializer.save() вызывает метод update сериализатора с аргументами instance и validated_data.

            return Response(serializer.data, status=status.HTTP_200_OK)
            # возвращает объект Response с:
            # данными сериализатора (serializer.data):
            # Это сериализованные данные объекта, которые будут отправлены в ответе.
            # статусом HTTP 200 OK: Это статус успешного запроса.

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Если данные не валидны (if serializer.is_valid(): вернул False),
    # эта строка создает и возвращает объект Response с:
    # ошибками сериализатора (serializer.errors): Это ошибки валидации, которые будут отправлены в ответе.
    # статусом HTTP 400 Bad Request: Это статус, указывающий, что запрос был некорректным.


