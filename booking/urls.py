from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reservation', views.reservation, name='reservation'),
    path('booking-submit', views.bookingSubmit, name='bookingSubmit'),
    path('user-panel', views.userPanel, name='userPanel'),
    path('user-update/<int:id>', views.userUpdate, name='userUpdate'),
    path('user-update-submit/<int:id>', views.userUpdateSubmit, name='userUpdateSubmit'),
    path('teacher-panel', views.teacherPanel, name='teacherPanel'),
]