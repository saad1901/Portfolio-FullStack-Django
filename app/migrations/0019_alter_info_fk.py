# Generated by Django 5.0.4 on 2025-01-16 10:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_info_fk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='info', to=settings.AUTH_USER_MODEL),
        ),
    ]
