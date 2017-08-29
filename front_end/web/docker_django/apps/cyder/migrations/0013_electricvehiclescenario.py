# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyder', '0012_auto_20170203_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectricVehicleScenario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nb_vehicles', models.IntegerField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('usermodel', models.ForeignKey(blank=True, to='cyder.UserModel', null=True)),
            ],
        ),
    ]
