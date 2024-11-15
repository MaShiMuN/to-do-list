from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Category
from api.serializers import CategorySerializer, CategoryCreateSerializer


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
