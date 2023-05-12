from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import WorkerCompanyViewSet, WorkerViewSet

router = DefaultRouter()
router.register("workercompany", WorkerCompanyViewSet,
                basename="workercompany")
router.register("workers", WorkerViewSet, basename="workers")
urlpatterns = [
    path('', include(router.urls)),
]
