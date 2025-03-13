from django.contrib import admin
from django import forms
from django.utils import timezone
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from .models import Position, Barber, Service, BarberService, BarberSchedule, Booking
from babel.dates import format_date
from rangefilter.filters import DateRangeFilter

class FutureDateWidget(forms.DateInput):
    input_type = 'date'

    def __init__(self, attrs=None, format=None):
        today_str = timezone.now().date().strftime("%Y-%m-%d")
        attrs = attrs or {}
        attrs.setdefault('min', today_str)
        super().__init__(attrs, format)

class TwentyFourHourTimeWidget(AdminTimeWidget):
    """ Виджет для отображения времени в 24-часовом формате """
    def format_value(self, value):
        if value is None:
            return ''
        if isinstance(value, str):
            return value
        return value.strftime('%H:%M')

def format_time_24h(obj):
    return f"{obj.start_time.strftime('%H:%M')} - {obj.end_time.strftime('%H:%M')}"
format_time_24h.short_description = "Графік"

def format_booking_time_24h(obj):
    return obj.time.strftime("%H:%M") if obj.time else "—"
format_booking_time_24h.short_description = "Час"

def format_booking_date_uk(obj):
    return format_date(obj.date, format="d MMMM yyyy", locale="uk").capitalize()
format_booking_date_uk.short_description = "Дата"

def get_service_price(obj):
    barber_service = BarberService.objects.filter(barber=obj.barber, service=obj.service).first()
    return f"{barber_service.price} грн" if barber_service else "—"
get_service_price.short_description = "Ціна послуги"

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("title",)

@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "is_active_today")
    list_editable = ("is_active_today",)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(BarberService)
class BarberServiceAdmin(admin.ModelAdmin):
    list_display = ("barber", "service", "price")

@admin.register(BarberSchedule)
class BarberScheduleAdmin(admin.ModelAdmin):
    list_display = ["barber", "day_of_week", format_time_24h]
    list_filter = ["barber", "day_of_week"]

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone", "barber", "service", get_service_price, format_booking_date_uk, format_booking_time_24h)
    list_filter = (
        ("date", DateRangeFilter),
        "barber",
    )
    search_fields = ("last_name", "phone")
