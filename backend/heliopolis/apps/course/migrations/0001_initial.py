# Generated by Django 4.2.1 on 2023-05-20 08:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("instructor", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=False)),
                (
                    "alias",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=False)),
                (
                    "alias",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(unique=True)),
                ("video", models.TextField()),
                (
                    "type",
                    models.PositiveIntegerField(
                        blank=True,
                        choices=[(1, "Content"), (2, "Quiz"), (3, "Assignment")],
                        default=1,
                        null=True,
                    ),
                ),
                ("image", models.ImageField(blank=True, null=True, upload_to="images")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Quiz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=False)),
                (
                    "alias",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("question", models.TextField()),
                ("correct_ans", models.IntegerField()),
                ("options", models.JSONField()),
                (
                    "section",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="course.lesson",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=False)),
                (
                    "alias",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(unique=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="course.category",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="course_owner",
                        to="instructor.instructor",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Chapter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=False)),
                (
                    "alias",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(unique=True)),
                (
                    "course",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="course.course",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=False)),
                (
                    "alias",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("file", models.FileField(upload_to="attachment")),
                (
                    "section",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="course.lesson",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
