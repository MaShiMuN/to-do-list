from rest_framework import serializers
from api.models import Task, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'


class TaskUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False)
    status = serializers.CharField(required=False)


class TaskCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

class CategoryCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)


class CategoryUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, required=False)