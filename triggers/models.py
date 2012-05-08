from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your models here.

class TriggerManager(models.Manager):
    def triggered(self):
        return self.get_query_set().filter(next_checkin__lte = datetime.now())

class Trigger(models.Model):
    INTERVAL_CHOICES = (('minutes', 'minutes'), ('hours', 'hours'), ('days', 'days'))

    objects = TriggerManager()

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
    
class Message(models.Model):
    """Holds email data to send out upon trigger"""
    owner = models.ForeignKey(User, related_name="message")
    to = models.TextField(max_length=1000, blank=False, null=False)
    subject = models.TextField(max_length=300)
    message = models.TextField(blank=False, null=False)
    
    def sendMessage(self):
        from django.core.mail import send_mail
        send_mail(self.subject, self.message, 'redmine@justfingdo.it', [to], fail_silently=False)
