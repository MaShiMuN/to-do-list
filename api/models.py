from django.db import models
from django.urls import reverse


class TaskStatuses(models.TextChoices):
    TO_DO = 'to_do'
    IN_PROGRESS = 'in_progress'
    PENDING = 'pending'
    DONE = 'done'


class Category(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# filtrovat po vsemu chto mojet pomoch taski i kategorii
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(choices=TaskStatuses.choices, default=TaskStatuses.TO_DO, max_length=20)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task-detail', args=[str(self.id)])


