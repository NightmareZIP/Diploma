from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Worker
from company.models import Company
from company.serializers import CompanySerializer

from .utils import get_worker


class WorkerCompanySerializer(serializers.ModelSerializer):
    company = CompanySerializer(required=True)

    class Meta:
        model = Worker
        read_only_fields = (
            "created_at",
            "head",
            # "company",
        ),
        fields = (
            'name',
            'last_name',
            'surname',
            'email',
            'contact_phone',
            'country',
            'user_id',
            'created_at',
            'head',
            'company',
        )

    def create(self, validated_data):
        company = validated_data.pop('company')

        worker = Worker.objects.create(**validated_data)
        worker.save()

        company['head'] = worker
        company['created_by'] = worker

        company = Company.objects.create(**company)
        # company.created_by = worker
        # company.head = worker
        company.save()
        worker.company = company
        worker.save()
        return worker


class WorkerSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True, required=False)

    class Meta:
        model = Worker
        read_only_fields = (
            "created_at",
            # "head",
            "company",
        ),
        fields = "__all__"

    # def create(self, validated_data):
    #     worker = Worker.object.create(**validated_data)
    #     return worker

    # def update(self, instance, validated_data)
