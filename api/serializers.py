from rest_framework import serializers

from app.models import Category, Course, Lesson


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    lessons = LessonListSerializer(many=True)

    class Meta:
        model = Course
        fields = "__all__"
