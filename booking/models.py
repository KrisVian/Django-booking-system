from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

RESERVATION_CHOICES = (
    ("Big room", "Big room"),
    ("Little room", "Little room"),
    ("Medium room", "Medium room"),
)

TIME_CHOICES = (
    ("8:00", "8:00"),
    ("9:00", "9:00"),
    ("10:00", "10:00"),
    ("11:00", "11:00"),
    ("12:00", "12:00"),
    ("13:00", "13,00"),
    ("14:00", "14:00"),
    ("15:00", "15:00"),
)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    reservation = models.CharField(max_length=60, choices=RESERVATION_CHOICES, default="Litte room")
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=20, choices=TIME_CHOICES, default="8:00")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"
    