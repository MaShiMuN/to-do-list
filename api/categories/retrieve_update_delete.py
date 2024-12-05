from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from api.service import get_category, patch_category, delete_category
from api.serializers import CategorySerializer


class RetrieveUpdateDeliteCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: CategorySerializer}
    )
    def get(self, request, category_id):
        return get_category(request, category_id)

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={200: CategorySerializer}
    )

    def patch(self, request, category_id):
        return patch_category(request, category_id)

    @swagger_auto_schema(
        responses={200: CategorySerializer}
    )
    def delete(self, request, category_id):
        return delete_category(request, category_id)
