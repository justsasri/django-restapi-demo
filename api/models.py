from functools import cached_property

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from .managers import CategoryManager
from .utils import unique_slugify


class User(AbstractUser):
    pass


class Category(MPTTModel):

    parent = TreeForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="children",
        help_text=_(
            "Categories, unlike tags, can have a hierarchy. You might have a "
            "Programming category, and under that have children categories for python,"
            "PHP, and JavaScript. Totally optional."
        ),
    )
    name = models.CharField(
        max_length=80,
        unique=True,
        verbose_name=_("Category Name"),
    )
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        editable=False,
        max_length=80,
    )
    objects = CategoryManager()

    class Meta:
        ordering = ["name"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        permissions = (
            ("import_category", _("Can import Category")),
            ("export_category", _("Can export Category")),
        )

    def __str__(self):
        return self.name

    @property
    def opts(self):
        return self.__class__._meta

    @property
    def title(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError("Parent category cannot be self.")
            if parent.parent and parent.parent == self:
                raise ValidationError("Cannot have circular Parents.")

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name)
        return super().save(*args, **kwargs)


class Course(models.Model):
    owner = models.ForeignKey(
        get_user_model(),
        related_name="courses",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name=_(
            "owner",
        ),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("name"),
        help_text=_("Course name"),
    )
    description = models.TextField(
        verbose_name=_("description"),
    )
    category = TreeForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Category"),
        help_text=_("Category used to group the lesson, totally optional."),
    )
    price = models.DecimalField(
        verbose_name=_("price"),
        help_text=_("Course price"),
        max_digits=15,
        decimal_places=2,
        validators=[
            MinValueValidator(25000.00),
            MaxValueValidator(1000000.00),
        ],
    )

    is_live = models.BooleanField(
        default=False,
        verbose_name=_("is live"),
        help_text=_("Is this course is live"),
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    last_modified_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"pk": self.pk})


class Lesson(models.Model):
    position = models.IntegerField(
        default=0,
        help_text=_("Lesson order or position"),
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        help_text=_("Related course"),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("title"),
        help_text=_("Lessons title"),
    )
    description = models.TextField(
        verbose_name=_("description"),
        help_text=_("Course description"),
    )
    duration = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(120),
        ],
    )

    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")
        index_together = ("course", "title")

    @cached_property
    def owner(self):
        return self.course.owner

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("lesson_detail", kwargs={"pk": self.pk})
