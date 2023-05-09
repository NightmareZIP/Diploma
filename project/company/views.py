from django.shortcuts import render

from rest_framework import viewsets, mixins
from django.contrib.auth.models import User

from .serializers import CompanySerializer
from .models import Company
from worker.models import Worker
from rest_framework import generics
from django.core.exceptions import PermissionDenied


class CompanyViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet,):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def get_queryset(self):
        user = self.request.user
        head = self.request.query_params.get('head')
        worker = Worker.objects.get(user_id=user)
        worker_cmp = worker.company
        if worker_id:
            return self.queryset.filter(id=self.request.user)
        return False

    def perform_update(self, serializer):
        # obj = self.get_object()

        # if self.request.user != obj.created_by:
        #     raise PermissionDenied('Wrong object owner')

        serializer.save()
