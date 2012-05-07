from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class TriggerManager(models.Manager):
    def get_query_set(self):
        return super(TriggerManager, self).get_query_set().filter(next_checkin__lte = datetime.now())

class Trigger(models.Model):
    INTERVAL_CHOICES = (('minutes', 60), ('hours', 3600), ('days', 86400))

    triggered = TriggerManager()

    description = models.TextField(max_length=300, blank=False, null=False)
    frequency = models.PositiveIntegerField(max_length=5)
    interval = models.CharField(max_length=10, choices=INTERVAL_CHOICES)
    next_checkin = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name="triggers")

    def checkin(self):
        self.triggered = False
        self.next_checkin = datetime.now() + timedelta(**{self.interval: self.frequency})

class TriggerAction(models.Model):
    """An action to be executed when the trigger fires"""
    trigger = models.ForeignKey(Trigger, related_name="actions")
