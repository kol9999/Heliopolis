# Generated by Django 4.2.1 on 2023-05-21 10:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0006_remove_chapter_slug_remove_lesson_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="video",
            field=models.FileField(upload_to="chapter"),
        ),
    ]
