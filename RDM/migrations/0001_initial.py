# Generated by Django 3.0.2 on 2020-01-13 10:55

import RDM.models
from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('YM', models.FloatField()),
                ('Density', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('auth', models.CharField(choices=[('private', 'private'), ('public', 'public')], default='private', max_length=10)),
                ('results', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('name', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isDone', models.BooleanField()),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('UX', models.BooleanField()),
                ('UZ', models.BooleanField()),
                ('RY', models.BooleanField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supports', to='RDM.Project')),
            ],
            options={
                'unique_together': {('name', 'project')},
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('Ax', models.FloatField()),
                ('Iy', models.FloatField()),
                ('H', models.FloatField()),
                ('Cy', models.FloatField()),
                ('type', models.CharField(default='Custom', max_length=20)),
                ('features', django.contrib.postgres.fields.jsonb.JSONField()),
                ('material', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='sections', to='RDM.Material')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='RDM.Project')),
            ],
            options={
                'unique_together': {('name', 'project')},
            },
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('UX1', models.BooleanField()),
                ('UZ1', models.BooleanField()),
                ('RY1', models.BooleanField()),
                ('UX2', models.BooleanField()),
                ('UZ2', models.BooleanField()),
                ('RY2', models.BooleanField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='releases', to='RDM.Project')),
            ],
            options={
                'unique_together': {('name', 'project')},
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.PositiveIntegerField()),
                ('X', models.FloatField()),
                ('Z', models.FloatField()),
                ('Fn', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=RDM.models.df_fl3, size=None)),
                ('Dp', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=RDM.models.df_fl3, size=None)),
                ('Rc', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=RDM.models.df_fl3, size=None)),
                ('Support', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='nodes', to='RDM.Support')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nodes', to='RDM.Project')),
            ],
            options={
                'unique_together': {('name', 'project')},
            },
        ),
        migrations.AddField(
            model_name='material',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='RDM.Project'),
        ),
        migrations.CreateModel(
            name='Bar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.PositiveIntegerField()),
                ('L', models.FloatField(default=0)),
                ('Ch', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20000), default=RDM.models.df_ch3, size=None)),
                ('Qg', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=RDM.models.df_fl3, size=None)),
                ('Ql', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=RDM.models.df_fl3, size=None)),
                ('Rg', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=RDM.models.df_fl3, size=None)),
                ('Rl', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=RDM.models.df_fl3, size=None)),
                ('EF', django.contrib.postgres.fields.jsonb.JSONField(default=RDM.models.df_json)),
                ('DP', django.contrib.postgres.fields.jsonb.JSONField(default=RDM.models.df_json)),
                ('S', django.contrib.postgres.fields.jsonb.JSONField(default=RDM.models.df_json)),
                ('EFm', django.contrib.postgres.fields.jsonb.JSONField(default=RDM.models.df_json)),
                ('DPm', django.contrib.postgres.fields.jsonb.JSONField(default=RDM.models.df_json)),
                ('Sm', django.contrib.postgres.fields.jsonb.JSONField(default=RDM.models.df_json)),
                ('N1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='N1', to='RDM.Node')),
                ('N2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='N2', to='RDM.Node')),
                ('Release', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='bars', to='RDM.Release')),
                ('Section', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='bars', to='RDM.Section')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bars', to='RDM.Project')),
            ],
            options={
                'unique_together': {('name', 'project')},
            },
        ),
        migrations.CreateModel(
            name='Pl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('FX', models.FloatField(default=0)),
                ('FZ', models.FloatField(default=0)),
                ('CY', models.FloatField(default=0)),
                ('nodes', models.ManyToManyField(blank=True, related_name='pls', to='RDM.Node')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pls', to='RDM.Project')),
            ],
            options={
                'unique_together': {('name', 'project')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='material',
            unique_together={('name', 'project')},
        ),
        migrations.CreateModel(
            name='Dl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('Axes', models.CharField(choices=[('G', 'Global'), ('L', 'Local')], default='G', max_length=1)),
                ('features', django.contrib.postgres.fields.jsonb.JSONField()),
                ('bars', models.ManyToManyField(blank=True, related_name='dls', to='RDM.Bar')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dls', to='RDM.Project')),
            ],
            options={
                'unique_together': {('name', 'project')},
            },
        ),
    ]
