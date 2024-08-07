from django.contrib import admin
from .models import Bike, Rent

@admin.register(Bike)  # декоратор регистрирует модель Bike в админке.
class BikeAdmin(admin.ModelAdmin):
    list_display = ('bike', 'status')  # Поля, которые будут отображаться в списке
    search_fields = ('bike', 'status')          # Поля для поиска
    list_filter = ('status',)


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ('user', 'bike', 'status', 'start_time', 'end_time', 'cost')




# admin.site.register(Bike, BikeAdmin)
