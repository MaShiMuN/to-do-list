from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Task
from api.serializers import TaskSerializer, TaskUpdateSerializer


class RetrieveUpdateDeleteTaskView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: TaskSerializer}
    )
    def get(self, request, task_id):
        task = Task.objects.filter(id=task_id, user=request.user).first()
        if not task:
            return Response({'error': 'Task not found'}, status=404)
        return Response(TaskSerializer(instance=task).data)

    @swagger_auto_schema(
        request_body=TaskUpdateSerializer,
        responses={200: TaskSerializer}
    )
    def patch(self, request, task_id):
        serializer = TaskUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = Task.objects.get(id=task_id)
        task.title = serializer.validated_data.get('title', task.title)
        task.description = serializer.validated_data.get('description', task.description)
        task.status = serializer.validated_data.get('status', task.status)
        task.save()
        return Response(TaskSerializer(instance=task).data)

    @swagger_auto_schema(
        responses={200: TaskSerializer}
    )
    def delete(self, request, task_id):
        task = Task.objects.get(id=task_id)
        task.delete()
        return Response({'status': 'ok'})
