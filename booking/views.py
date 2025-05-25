from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import *
from django.contrib import messages

def index(request):
    return render(request, "index.html",{})

def reservation(request):
    weekdays = validWeekday(26)

    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == 'POST':
        reservation = request.POST.get('reservation')
        day = request.POST.get('day')
        if reservation == None:
            messages.success(request, "Choose reservation.")
            return redirect('reservation')
        
        request.session['day'] = day
        request.session['reservation'] = reservation

        return redirect('bookingSubmit')
    

    return render(request, 'reservation.html', {
        'weekdays':weekdays,
        'validateWeekdays':validateWeekdays,
    })

def bookingSubmit(request):
    user = request.user
    times = [
        "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=26)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    day = request.session.get('day')
    reservation = request.session.get('reservation')

    hour = checkTime(times, day)
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if reservation != None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date == 'Tuesday' or date == 'Wednesday' or date == 'Thursday' or date == 'Friday':
                    if Reservation.objects.filter(day=day).count() < 11:
                        if Reservation.objects.filter(day=day, time=time).count() < 1:
                            ReservationForm = Reservation.objects.get_or_create(
                                user = user,
                                reservation = reservation,
                                day = day,
                                time = time,
                            )
                            messages.success(request, "Reservation successful.")
                            return redirect('index')
                        else:
                            messages.success(request, "The selected time has been reserved already.")
                    else:
                        messages.success(request, "The selected day is full.")
                else:
                    messages.success(request, "The selected date is incorrect.")
            else:
                    messages.success(request, "The selected date isn't in the correct time period.")
        else:
            messages.success(request, "Please select.")


    return render(request, 'bookingSubmit.html', {
        'times':hour,
    })

def userPanel(request):
    user =request.user
    reservations = Reservation.objects.filter(user=user).order_by('day', 'time')
    return render(request, 'userPanel.html', {
        'user':user,
        'reservations':reservations,
    })

def userUpdate(request, id):
    reservation = Reservation.objects.get(pk=id)
    userdatepicked = reservation.day

    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')

    delta24 = (userdatepicked).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')

    weekdays = validWeekday(26)

    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == 'POST':
        reservation = request.POST.get('reservation')
        day = request.POST.get('day')

        request.session['day'] = day
        request.session['reservation'] = reservation

        return redirect('userUpdateSubmit', id=id)
    
    return render(request, 'userUpdate.html', {
        'weekdays':weekdays,
        'validateWeekdays':validateWeekdays,
        'delta24':delta24,
        'id':id,
    })

def userUpdateSubmit(request, id):
    user = request.user
    times = [
        "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=26)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    day = request.session.get('day')
    reservation = request.session.get('reservation')

    hour = checkEditTime(times, day, id)
    reservation = Reservation.objects.get(pk=id)
    userSelectedTime = reservation.time
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if reservation != None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date == 'Tuesday' or date == 'Wednesday' or date == 'Thursday' or date == 'Friday':
                    if Reservation.objects.filter(day=day).count() < 11:
                        if Reservation.objects.filter(day=day, time=time).count() < 1 or userSelectedTime == time:
                            ReservationForm = Reservation.objects.filter(pk=id).update(
                                user = user,
                                reservation = reservation,
                                day = day,
                                time = time,
                            )
                            messages.success(request, "Reservation edited.")
                            return redirect('index')
                        else:
                            messages.success(request, "The selected time has been reserved before.")
                    else:
                        messages.success(request, "The selected day is full.")
                else:
                    messages.success(request, "The selected date is incorrect.")
            else:
                    messages.success(request, "The selected date isn't in the correct time.")
        else:
            messages.success(request, "Please select.")
        return redirect('userPanel')
    
    return render(request, 'userUpdateSubmit.html', {
        'times':hour,
        'id':id,
    })

def teacherPanel(request):
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=26)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime
    items = Reservation.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')


    return render(request, 'teacherPanel.html', {
        'items':items,
    })


def dayToWeekday(x):
    z = datetime.strptime(x, "%Y-%m-%d")
    y = z.strftime('%A')
    return y

def validWeekday(days):
    today = datetime.now()
    weekdays = []
    for i in range (0, days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        if y == 'Monday' or y == 'Tuesday' or y == 'Wednesday' or y == 'Thursday' or y == 'Friday':
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays

def isWeekdayValid(x):
    validateWeekdays = []
    for j in x:
        if Reservation.objects.filter(day=j).count() < 10:
            validateWeekdays.append(j)
    return validateWeekdays

def checkTime(times, day):
    x = []
    for k in times:
        if Reservation.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x

def checkEditTime(times, day, id):
    x = []
    reservation = Reservation.objects.get(pk=id)
    time = reservation.time
    for k in times:
        if Reservation.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x



# Create your views here.
