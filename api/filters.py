from django_filters.rest_framework.filterset import FilterSet

from .models import Course


class CourseAPIFilterset(FilterSet):
    """Course REST API filterset, commonly used in list"""

    class Meta:
        model = Course
        fields = ["is_live", "created_at"]
