from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, EventType
from company.models import Company
from worker.models import Worker
from worker.serializers import WorkerSerializer

from company.serializers import CompanySerializer

from worker.utils import get_worker


class EventTypeSerializer(serializers.ModelSerializer):
    """_summary_
        Серриалайзер для ReadOnly
    Args:
        serializers (_type_): _description_
    """

    class Meta:
        model = EventType
        read_only_fields = (
            'name',
            'id',
            'color',
        ),
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    event_type = EventTypeSerializer()
    created_by = WorkerSerializer(required=True)
    created_for = WorkerSerializer(required=True)

    class Meta:
        model = Event
        read_only_fields = (
            "id",
            "created_at",
        ),
    fields = "__all__"

    # def create(self, validated_data):

    #     return worker

    # def to_representation(self, instance):


class HeadEventSerializer(serializers.ModelSerializer):
    """_summary_
        Создание событий для подчиненных
    Args:
        serializers (_type_): _description_

    Returns:
        _type_: _description_
    """
    company_data = CompanySerializer(required=True)

    class Meta:
        model = Worker
        read_only_fields = (
            "user_id",
            "created_at",
            "head",
            "company",
        ),
        fields = "__all__"

    def create(self, validated_data):
        company_data = validated_data.pop('company_data')
        worker = Worker.object.create(**validated_data)
        worker.save()
        company = Company.object.create(**company_data)
        company.created_by = worker.id
        company.head = worker.id
        company.save()
        worker.company = company.id
        worker.save()
        return worker
