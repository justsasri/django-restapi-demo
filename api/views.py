from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers import CategorySerializer, CourseSerializer, LessonSerializer
from app.models import Category, Course, Lesson

from .filters import CourseAPIFilterset
from .permissions import IsOwnerOrAdminOrReadOnly


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.select_related("parent").all()
    serializer_class = CategorySerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related("category").all()
    serializer_class = CourseSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    filterset_class = CourseAPIFilterset
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "price"]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(description="Toogle course publicity.", request=None, responses=None)
    @action(methods=["PUT"], detail=True)
    def toogle_live(self, request, pk):
        obj = self.get_object()
        obj.is_live = not obj.is_live
        obj.save()
        serializer = self.get_serializer(instance=obj)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.validated_data["owner"] = self.request.user
        return super().perform_create(serializer)


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.select_related("course").all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    search_fields = ["title", "description"]
