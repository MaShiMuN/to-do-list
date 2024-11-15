# from django.db.models import Q
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework.response import Response
#
# from api.models import Task
# from api.serializers import TaskSerializer
#
#
# @swagger_auto_schema(
#     responses={200: TaskSerializer(many=True)}
# )
# def get_filtered_tasks(self, request):
#     queryset = Task.objects.filter(user=request.user)
#     search_query = request.query_params.get('query', None)
#
#     if search_query:
#         queryset = queryset.filter(
#             Q(title__icontains=search_query) | Q(description__icontains=search_query)
#         )
