# Generated by Django 5.0.7 on 2024-08-18 05:17

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0005_rename_gender_user_area_rename_name_user_id_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relatorio',
            name='data',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='relatorio',
            name='horario',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='user',
            name='area',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
