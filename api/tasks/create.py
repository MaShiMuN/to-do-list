from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Task
from api.serializers import TaskSerializer, TaskCreateSerializer


class ListCreateTaskView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: TaskSerializer(many=True)}
    )
    def get(self, request):
        queryset = Task.objects.filter(user=request.user)
        search_query = request.query_params.get('query', None)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )

        return Response({"tasks": [TaskSerializer(instance=task).data for task in queryset]})

    @swagger_auto_schema(
        request_body=TaskSerializer,
        responses={201: TaskSerializer}
    )
    def post(self, request):
        user = request.user
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = Task.objects.create(
            title=serializer.validated_data['title'],
            description=serializer.validated_data['description'],
            user=user
        )
        return Response(TaskSerializer(instance=task).data, status=201)
