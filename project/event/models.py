from django.db import models
from worker.models import Worker


class Event(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        Worker, related_name='worker_by', on_delete=models.CASCADE)
    created_for = models.ForeignKey(
        Worker, related_name='worker_for', on_delete=models.CASCADE)
    comment = models.TextField()
    period = models.IntegerField(default=0)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return '%s' % self.name
