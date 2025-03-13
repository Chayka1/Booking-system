from django.urls import path
from .views import (
    user_info_view,
    booking_details_view,
    thank_you_view,
    booking_api,
    barbers_for_date_api,
    delete_booking_view,
    edit_booking_view,
)

urlpatterns = [
    path('', user_info_view, name='user_info'),
    path('details/', booking_details_view, name='booking_details'),
    path('thank-you/<int:booking_id>/', thank_you_view, name='thank_you'),
    path('api/booking/', booking_api, name='booking_api'),
    path('api/barbers-for-date/', barbers_for_date_api, name='barbers_for_date_api'),
    path('delete-booking/<int:booking_id>/', delete_booking_view, name='delete_booking'),
    path('edit-booking/<int:booking_id>/', edit_booking_view, name='edit_booking'),
]
