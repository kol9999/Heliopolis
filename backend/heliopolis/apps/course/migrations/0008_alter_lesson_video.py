# Generated by Django 4.2.1 on 2023-05-22 08:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0007_alter_lesson_video"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="video",
            field=models.FileField(blank=True, null=True, upload_to="chapter"),
        ),
    ]
