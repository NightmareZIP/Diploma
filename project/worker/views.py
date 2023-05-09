from django.shortcuts import render

from rest_framework import viewsets, mixins
from django.contrib.auth.models import User

from .serializers import WorkerSerializer, WorkerCompanySerializer
from company.models import Company
from .utils import get_worker
from worker.models import Worker
from rest_framework import generics
from django.core.exceptions import PermissionDenied


class WorkerCompanyViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = WorkerCompanySerializer
    queryset = Worker.objects.all()
    def perform_create(self, serializer):
        serializer.save()


class WorkerViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet,):

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
