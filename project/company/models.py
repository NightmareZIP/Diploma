from django.db import models
from django.contrib.auth.models import User
from worker.models import Worker
from django.core.validators import RegexValidator


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Телефон формата: '+999999999'.")
    contact_phone = models.CharField(
        validators=[phone_regex], unique=True, max_length=12, blank=True)
    email = models.EmailField(unique=True)

    created_by = models.ForeignKey(
        Worker, related_name='worker_created', on_delete=models.CASCADE)
    head = models.ForeignKey(
        Worker, related_name='worker_head', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % self.name
