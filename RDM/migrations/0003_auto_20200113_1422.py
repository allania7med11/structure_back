# Generated by Django 3.0.2 on 2020-01-13 14:22

import RDM.models
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RDM', '0002_auto_20200113_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='variables',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=RDM.models.df_json),
        ),
    ]
