# Generated by Django 2.2.6 on 2019-10-08 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20191008_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='type',
            field=models.CharField(choices=[('RCT', 'Rectangular'), ('RCTH', 'Rectangular Hollow'), ('CRC', 'Circular'), ('CRCH', 'Circular Hollow'), ('TSC', 'T Section'), ('ISC', 'I Section'), ('CST', 'Custom')], default='Custom', max_length=20),
        ),
    ]