from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        read_only_fields = (
            "created_by",
            "head",
            "created_at",
        ),
        fields = (
            'name',
            'country',
            'place',
            'contact_person',
            'contact_phone',
            'email',
            'inn',
        )
