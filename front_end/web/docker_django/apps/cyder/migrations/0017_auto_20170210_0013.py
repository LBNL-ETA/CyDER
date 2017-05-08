# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cyder', '0016_auto_20170207_0654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('last_modified', models.DateTimeField(null=True, blank=True)),
                ('in_progress', models.BooleanField(default=False)),
                ('result_available', models.BooleanField(default=False)),
                ('status', models.TextField(null=True, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectModels',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model', models.ForeignKey(blank=True, to='cyder.Model', null=True)),
                ('project', models.ForeignKey(blank=True, to='cyder.Project', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='model',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='user',
        ),
        migrations.RemoveField(
            model_name='currentcalibration',
            name='impedance_a',
        ),
        migrations.RemoveField(
            model_name='currentcalibration',
            name='impedance_b',
        ),
        migrations.RemoveField(
            model_name='currentcalibration',
            name='impedance_c',
        ),
        migrations.RemoveField(
            model_name='electricvehiclescenario',
            name='usermodel',
        ),
        migrations.RemoveField(
            model_name='noderesult',
            name='usermodel',
        ),
        migrations.AddField(
            model_name='currentcalibration',
            name='impedance_imag',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='currentcalibration',
            name='impedance_real',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='UserModel',
        ),
        migrations.AddField(
            model_name='electricvehiclescenario',
            name='project_model',
            field=models.OneToOneField(null=True, blank=True, to='cyder.ProjectModels'),
        ),
        migrations.AddField(
            model_name='noderesult',
            name='project_model',
            field=models.ForeignKey(blank=True, to='cyder.ProjectModels', null=True),
        ),
    ]
