from django.shortcuts import render
from datetime import date, datetime, timedelta
from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from worker.utils import get_worker
from rest_framework.decorators import action
from .serializers import EventTypeSerializer, EventSerializer
from .models import Event, EventType
from worker.models import Worker
from rest_framework import generics
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework.response import Response


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

    @action(detail=False)
    def get_events(self, request):
        """Получение событий работника, при этом в запрос попадают так же периодические события

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Получим непиродические события
        q_set = self.get_queryset()
        date_from = self.request.query_params.get('date_from')
        print('from ', date_from)
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_to = self.request.query_params.get('date_to')
        date_to = datetime.strptime(date_to,  "%Y-%m-%d")

        not_period = q_set.filter(
            date_from__gte=date_from, date_to__lte=date_to, period=0)

        # Получим все периодические события
        period = q_set.filter(~Q(period=0), date_to__lte=date_to)
        period_copy = period.all()
        delta = date_to - date_from   # returns timedelta
        days = []
        for i in range(delta.days + 1):
            day = date_from + timedelta(days=i)
            days.append(day)
        for event in period:
            excl = True
            for day in days:
                day_from = event.date_from
                dif = day_from.replace(tzinfo=None) - day
                if dif.days % event.period == 0:
                    excl = False
                    break
                    print(event.id)
            if excl:
                period_copy.exclude(id=event.id)

        event_combine = period_copy | not_period
        self.check_object_permissions(self.request, event_combine)

        serializer = self.get_serializer(event_combine, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # print(self.request.data['event_type'])
        # event_type = EventType.objects.get(id=event_type)
        created_by = Worker.objects.get(user_id=self.request.user)
        serializer.save(created_by=created_by,
                        created_for=created_by,)

    def perform_update(self, serializer):
        # print(self.request.data['event_type'])
        # event_type = EventType.objects.get(id=event_type)
        created_by = Worker.objects.get(user_id=self.request.user)
        serializer.save(created_by=created_by,
                        created_for=created_by,)


class EventTypeViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):

    serializer_class = EventTypeSerializer
    queryset = EventType.objects.all()
