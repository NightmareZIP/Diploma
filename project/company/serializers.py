from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company
from worker.models import Worker


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        read_only_fields = (
            "created_at",
            # "head",
            "company",
        ),
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    # head = WorkerSerializer(required=False, read_only=True)

    class Meta:
        model = Company
        read_only_fields = (
            "created_by",
            # "head",
            "created_at",
        )
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
