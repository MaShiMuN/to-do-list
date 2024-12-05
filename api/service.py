from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Category
from api.serializers import CategorySerializer, CategoryUpdateSerializer


def get_category(self, request, category_id):
    category = Category.objects.filter(id=category_id, user=request.user).first()
    if not category:
        return Response({'error': 'Category not found'}, status=404)
    return Response(CategorySerializer(instance=category).data)

def patch_category(self, request, category_id):
    category = Category.objects.get(id=category_id, user=request.user)
    serializer = CategoryUpdateSerializer(category_id, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    category.name = serializer.validated_data.get('name', category.name)
    category.save()
    return Response(CategorySerializer(instance=category).data)

def delete_category(self, request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return Response({'status': 'ok'})


