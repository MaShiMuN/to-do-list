from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from api.models import Task, Category
from rest_framework import generics
from api.serializers import TaskSerializer, TaskUpdateSerializer, TaskCreateSerializer, CategorySerializer, CategoryCreateSerializer, CategoryUpdateSerializer
from drf_yasg.utils import swagger_auto_schema



class CheckHealthView(APIView):
    def get(self, request):
        return Response({'status': 'ok'})


# class CheckBookView(APIView):
#     def get(self, request):
#         books = Book.objects.all()
#         return Response({"books": [BookSerializer(instance=book).data for book in books]})

    # def post(self, request):
    #     data = request.data
    #     book = Book.objects.create(title=data['title'])
    #     return Response(BookSerializer(instance=book).data, status=201)


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


class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = ['priority']

    @swagger_auto_schema(
        responses={200: TaskSerializer}
    )
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class CategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(
        responses={200: CategorySerializer}
    )
    def get(self, request):
        name = request.query_params.get('name', None)
        queryset = Category.objects.filter(user=request.user)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if not queryset.exists():
            return Response({"categories": []})

        return Response({"categories": [CategorySerializer(instance=category).data for category in queryset]})

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={201: CategorySerializer}
    )
    def post(self, request):
        serializer = CategoryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = Category.objects.create(
            name=serializer.validated_data['name'],
            user=request.user
        )
        return Response(CategorySerializer(instance=category).data, status=201)


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @swagger_auto_schema(
        responses={200: TaskSerializer}
    )
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class RetrieveUpdateDeliteCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: CategorySerializer}
    )
    def get(self, request, category_id):
        category = Category.objects.filter(id=category_id, user=request.user).first()
        if not category:
            return Response({'error': 'Category not found'}, status=404)
        return Response(CategorySerializer(instance=category).data)

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={200: CategorySerializer}
    )
    def patch(self, request, category_id):
        category = Category.objects.get(id=category_id, user=request.user)
        serializer = CategoryUpdateSerializer(category_id, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        category.name = serializer.validated_data.get('name', category.name)
        category.save()
        return Response(CategorySerializer(instance=category).data)

    @swagger_auto_schema(
        responses={200: CategorySerializer}
    )
    def delete(self, request, category_id):
        category = Category.objects.get(id=category_id)
        category.delete()
        return Response({'status': 'ok'})
