from django.shortcuts import render

from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from rest_framework.decorators import action

from .serializers import WorkerSerializer, WorkerCompanySerializer
from company.models import Company
from .utils import get_worker
from worker.models import Worker
from rest_framework import generics
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response


class WorkerCompanyViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = WorkerCompanySerializer
    queryset = Worker.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class WorkerViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, viewsets.GenericViewSet,
                    mixins.UpdateModelMixin, mixins.DestroyModelMixin,):

    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()

    def get_queryset(self):

        worker_id = get_worker(self.request.user)
        return self.queryset.filter(id=worker_id)

    def perform_create(self, serializer):
        # obj = self.get_object()

        # company = Company.objects.get(pk=obj.company)
        company_id = self.request.data['company']
        company = Company.objects.get(id=company_id)
        head = company.head
        serializer.save(head=head,  company=company)

    def perform_update(self, serializer):
        worker_id = get_worker(self.request.user)
        obj = self.get_object()

        if worker_id != obj.id:
            raise PermissionDenied('Wrong object owner')

        serializer.save()

    @action(detail=False)
    def get_workers(self, request):
        # Получим непиродические события
        q_set = self.get_queryset()
        company = self.request.user.worker_user.company
        workers = Worker.objects.all().filter(company=company)
        print(workers)
        self.check_object_permissions(self.request, workers)
        serializer = self.get_serializer(workers, many=True)
        return Response(serializer.data)
