# bikes/urls.py

from django.urls import path
from .views import BikeListView, RentBikeView, ReturnBikeView

urlpatterns = [
    path('bikes/', BikeListView.as_view(), name='bike-list'),
    path('rent/', RentBikeView.as_view(), name='rent-bike'),
    path('return/<int:bike_id>/', ReturnBikeView.as_view(), name='return-bike'),
]
