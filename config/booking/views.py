from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import UserInfoForm, BookingDetailsForm
from .models import Booking, Barber, BarberService, BarberSchedule
from datetime import datetime, time, timedelta

@csrf_exempt
def user_info_view(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = form.cleaned_data['first_name']
            request.session['last_name'] = form.cleaned_data['last_name']
            request.session['phone'] = form.cleaned_data['phone']
            return redirect('booking_details')
    else:
        form = UserInfoForm()
    return render(request, 'booking/user_info.html', {'form': form})

@csrf_exempt
def booking_details_view(request):
    first_name = request.session.get('first_name')
    last_name = request.session.get('last_name')
    phone = request.session.get('phone')

    if not (first_name and last_name and phone):
        return redirect('user_info')

    if request.method == 'POST':
        form = BookingDetailsForm(request.POST)
        if form.is_valid():
            barber_id = form.cleaned_data['barber']
            service_id = form.cleaned_data['service']
            date_obj = form.cleaned_data['date']
            time_obj = form.cleaned_data['time']

            if not barber_id:
                return JsonResponse({'error': 'Barber is required'}, status=400)

            barber_service = BarberService.objects.filter(barber_id=barber_id, service_id=service_id).first()
            price = barber_service.price if barber_service else 0

            booking = Booking.objects.create(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                barber_id=barber_id,
                service_id=service_id,
                date=date_obj,
                time=time_obj,
                price=price
            )
            return redirect('thank_you', booking.id)

    else:
        form = BookingDetailsForm()

    barbers = Barber.objects.filter(is_active_today=True)

    return render(request, 'booking/booking_details.html', {
        'form': form,
        'barbers': barbers
    })



@csrf_exempt
def thank_you_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking/thank_you.html', {'booking': booking})

@csrf_exempt
def booking_api(request):
    barber_id = request.GET.get('barber_id')
    date_str = request.GET.get('date')
    if not barber_id:
        return JsonResponse({'error': 'No barber_id provided'}, status=400)
    try:
        barber_id = int(barber_id)
        bservices = BarberService.objects.filter(barber_id=barber_id).select_related('service')
        services_data = []
        for bs in bservices:
            services_data.append({
                'id': bs.service.id,
                'name': bs.service.name,
                'price': float(bs.price)
            })
        times_data = []
        if date_str:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            weekday = date_obj.weekday()
            schedules = BarberSchedule.objects.filter(barber_id=barber_id, day_of_week=str(weekday))
            if schedules.exists():
                sch = schedules.first()
                start_time = sch.start_time
                end_time = sch.end_time
                booked = Booking.objects.filter(barber_id=barber_id, date=date_obj).values_list('time', flat=True)
                current_time = datetime.combine(date_obj, start_time)
                end_datetime = datetime.combine(date_obj, end_time)
                shop_start = time(8, 0)
                shop_end = time(20, 0)
                while current_time < end_datetime:
                    if shop_start <= current_time.time() <= shop_end:
                        if current_time.time() not in booked:
                            times_data.append(current_time.strftime('%H:%M'))
                    current_time += timedelta(hours=1)
        schedules_all = BarberSchedule.objects.filter(barber_id=barber_id)
        workdays = [int(s.day_of_week) for s in schedules_all]
        return JsonResponse({
            'services': services_data,
            'times': times_data,
            'workdays': workdays
        })
    except ValueError:
        return JsonResponse({'error': 'Invalid barber_id or date format'}, status=400)

@csrf_exempt
def barbers_for_date_api(request):
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'error': 'No date provided'}, status=400)

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        weekday = date_obj.weekday()
        
        schedules = BarberSchedule.objects.filter(day_of_week=str(weekday), barber__is_active_today=True)
        
        free_barbers = set()
        for sch in schedules:
            barber = sch.barber
            if not barber.is_active_today:
                continue

            barber_id = barber.id
            start_time = sch.start_time
            end_time = sch.end_time

            booked = Booking.objects.filter(barber_id=barber_id, date=date_obj).values_list('time', flat=True)
            current_time = datetime.combine(date_obj, start_time)
            end_datetime = datetime.combine(date_obj, end_time)

            shop_start = time(8, 0)
            shop_end = time(20, 0)
            free_count = 0

            while current_time < end_datetime:
                if shop_start <= current_time.time() <= shop_end:
                    if current_time.time() not in booked:
                        free_count += 1
                current_time += timedelta(hours=1)

            if free_count > 0:
                free_barbers.add(barber_id)

        data = [
            {'id': b.id, 'name': b.name, 'position': b.position.title}
            for b in Barber.objects.filter(id__in=free_barbers, is_active_today=True)
        ]

        return JsonResponse({'barbers': data})
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)


@csrf_exempt
def delete_booking_view(request, booking_id):
    if request.method == "POST":
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.delete()
            return JsonResponse({"status": "success", "message": "Бронирование удалено"})
        except Booking.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Бронирование не найдено"}, status=404)
    return JsonResponse({"status": "error", "message": "Неверный запрос"}, status=400)

@csrf_exempt
def edit_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = BookingDetailsForm(request.POST)
        if form.is_valid():
            barber_id = form.cleaned_data['barber']
            service_id = form.cleaned_data['service']
            date_obj = form.cleaned_data['date']
            time_obj = form.cleaned_data['time']

            barber_service = BarberService.objects.filter(barber_id=barber_id, service_id=service_id).first()
            price = barber_service.price if barber_service else 0

            new_booking = Booking.objects.create(
                first_name=booking.first_name,
                last_name=booking.last_name,
                phone=booking.phone,
                barber_id=barber_id,
                service_id=service_id,
                date=date_obj,
                time=time_obj,
                price=price
            )

            booking.delete()

            return redirect('thank_you', new_booking.id)

    else:
        form = BookingDetailsForm(initial={
            'barber': booking.barber.id,
            'service': booking.service.id,
            'date': booking.date,
            'time': booking.time
        })

    barbers = Barber.objects.all()
    return render(request, 'booking/booking_details.html', {
        'form': form,
        'booking': booking,
        'barbers': barbers
    })

