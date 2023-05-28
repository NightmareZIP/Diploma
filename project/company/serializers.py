from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company
from worker.models import Worker


class CompanySerializer(serializers.ModelSerializer):
    """Класс сериалайзера компании
    """
    class Meta:
        #Сущность
        model = Company
        #поля доступные только для чтения
        read_only_fields = (
            "created_by",
            # "head",
            "created_at",
        )
        #Список полей, обрабатывыемых сериалайзером
        fields = (
            'id',
            'name',
            'country',
            'place',
            'contact_person',
            'contact_phone',
            'email',
            'inn',
            # 'head',
        )
