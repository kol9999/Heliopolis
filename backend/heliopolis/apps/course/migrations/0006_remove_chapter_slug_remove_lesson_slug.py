# Generated by Django 4.2.1 on 2023-05-21 07:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0005_alter_course_owner_alter_course_title"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chapter",
            name="slug",
        ),
        migrations.RemoveField(
            model_name="lesson",
            name="slug",
        ),
    ]
