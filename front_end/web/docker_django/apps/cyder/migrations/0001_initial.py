# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CalibrationData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('p_a', models.FloatField(null=True, blank=True)),
                ('p_b', models.FloatField(null=True, blank=True)),
                ('p_c', models.FloatField(null=True, blank=True)),
                ('q_a', models.FloatField(null=True, blank=True)),
                ('q_b', models.FloatField(null=True, blank=True)),
                ('q_c', models.FloatField(null=True, blank=True)),
                ('voltage_a', models.FloatField(null=True, blank=True)),
                ('voltage_b', models.FloatField(null=True, blank=True)),
                ('voltage_c', models.FloatField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CalibrationHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(null=True, blank=True)),
                ('updated', models.BooleanField(default=False)),
                ('calibration_algorithm', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CalibrationResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('impedance_a', models.FloatField(null=True, blank=True)),
                ('impedance_b', models.FloatField(null=True, blank=True)),
                ('impedance_c', models.FloatField(null=True, blank=True)),
                ('calibration', models.OneToOneField(null=True, blank=True, to='cyder.CalibrationHistory')),
            ],
        ),
        migrations.CreateModel(
            name='CurrentCalibration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('impedance_a', models.FloatField(null=True, blank=True)),
                ('impedance_b', models.FloatField(null=True, blank=True)),
                ('impedance_c', models.FloatField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=50, null=True, blank=True)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('lon', models.FloatField(null=True, blank=True)),
                ('breaker_name', models.CharField(max_length=50, null=True, blank=True)),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('area', models.CharField(max_length=50, null=True, blank=True)),
                ('region', models.CharField(max_length=50, null=True, blank=True)),
                ('zip_code', models.CharField(max_length=50, null=True, blank=True)),
                ('version', models.CharField(max_length=50, null=True, blank=True)),
                ('upmu_location', models.CharField(max_length=50, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='currentcalibration',
            name='model',
            field=models.OneToOneField(null=True, blank=True, to='cyder.Model'),
        ),
        migrations.AddField(
            model_name='calibrationhistory',
            name='model',
            field=models.ForeignKey(blank=True, to='cyder.Model', null=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='calibration',
            field=models.OneToOneField(null=True, blank=True, to='cyder.CalibrationHistory'),
        ),
    ]
