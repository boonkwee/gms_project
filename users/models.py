from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class SystemUser(AbstractUser):
    # Add additional fields for password expiry
    password_expiry_date = models.DateField(blank=True, null=True, verbose_name='Password Expiry')
    password_expiry_notification_date = models.DateField(blank=True, null=True, 
                                                         verbose_name='Password Expiry Notification')

    def is_password_expired(self):
        if self.password_expiry_date and self.password_expiry_date < timezone.now().date():
            return True
        return False

    def is_password_expiry_notification_required(self):
        if self.password_expiry_notification_date and self.password_expiry_notification_date < timezone.now().date():
            return True
        return False

    def set_password_expiry(self, expiry_days, notification_days):
        self.password_expiry_date = timezone.now().date() + timedelta(days=expiry_days)
        self.password_expiry_notification_date = timezone.now().date() + timedelta(days=notification_days)
