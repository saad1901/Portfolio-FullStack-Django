# Generated by Django 5.0.4 on 2024-12-30 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_projects_image_alter_projects_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='username',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
