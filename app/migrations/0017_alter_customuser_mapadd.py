# Generated by Django 5.0.4 on 2025-01-02 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_rename_time_news_timex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='mapadd',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
    ]