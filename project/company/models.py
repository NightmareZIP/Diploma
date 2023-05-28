#подключаем библиотеки
from django.db import models
from django.contrib.auth.models import User
from worker.models import Worker
from django.core.validators import RegexValidator


class Company(models.Model):
    """Сущнсоть компании

    Args:
        массив аргументов сщунсоти

    Returns:
        Объект Model
    """
    #создание аргумента сущности
    name = models.CharField(max_length=255, unique=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    inn = models.CharField(max_length=255, blank=False, null=False)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Телефон формата: '+999999999'.")
    contact_phone = models.CharField(
        validators=[phone_regex], unique=True, max_length=12, blank=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """_summary_

        Returns:
            string: наименование экземпляра в сущности для админ панели
        """
        return '%s' % self.name
