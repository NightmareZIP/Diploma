from django.shortcuts import render

from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from worker.utils import get_worker

from .serializers import EventTypeSerializer, EventSerializer
from .models import Event, EventType
from worker.models import Worker
from rest_framework import generics
from django.core.exceptions import PermissionDenied


class EventViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """_summary_
        Класс представление для работы с событиями
    Args:
        mixins (_type_): _description_
        mixins (_type_): _description_
        mixins (_type_): _description_
        mixins (_type_): _description_
        viewsets (_type_): _description_

    Returns:
        _type_: _description_
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_queryset(self):
        worker_id = get_worker(self.request.user)
        # TODO Добавить обработку по url дял начальника
        if worker_id:
            return self.queryset.filter(created_for=worker_id)
        return False


class EventTypeViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):

    serializer_class = EventTypeSerializer
    queryset = EventType.objects.all()
