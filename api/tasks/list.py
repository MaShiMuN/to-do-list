from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from api.models import Task
from api.serializers import TaskSerializer


class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = ['priority']

    @swagger_auto_schema(
        responses={200: TaskSerializer}
    )
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
