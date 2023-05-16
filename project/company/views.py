from django.shortcuts import render

from rest_framework import viewsets, mixins
from django.contrib.auth.models import User

from .serializers import CompanySerializer
from .models import Company
from worker.models import Worker
from rest_framework import generics
from django.core.exceptions import PermissionDenied


class CompanyViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     ):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def get_queryset(self):
        # company_id = self.request.data['company']

        user = self.request.user
        worker = Worker.objects.get(user_id=user)
        cmp_id = worker.company.id

        if worker:
            return self.queryset.filter(id=cmp_id)
        return False

    def perform_update(self, serializer):
        user = self.request.user
        worker = Worker.objects.get(user_id=user)
        cmp_head = worker.is_head

        cmp_id = int(self.request.parser_context['kwargs']['pk'])
        print([cmp_head, worker.company.id, cmp_id])

        if not cmp_head or worker.company.id != cmp_id:
            raise PermissionDenied('Wrong object owner')

        serializer.save()
