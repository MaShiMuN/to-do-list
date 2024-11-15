"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from api.views import CheckHealthView
from api.categories.retrieve_update_delete import RetrieveUpdateDeliteCategoryView
from api.categories.list_create import CategoryListCreateView
from api.tasks.retrieve_update_delete import RetrieveUpdateDeleteTaskView
from api.tasks.create import ListCreateTaskView
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health', CheckHealthView.as_view(), name='health'),
    path('categories', CategoryListCreateView.as_view(), name='category'),
    path('categories/<int:category_id>', RetrieveUpdateDeliteCategoryView.as_view(), name='category'),
    path('tasks', ListCreateTaskView.as_view(), name='task'),
    path('tasks/<int:task_id>', RetrieveUpdateDeleteTaskView.as_view(), name='task'),
    path('auth/', include((
        [
            path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
        ], 'auth'
    ))),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('book', CheckBookView.as_view(), name='book'),
]
