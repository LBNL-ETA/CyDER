# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyder', '0011_usermodel_result_available'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calibrationdata',
            name='p_a',
        ),
        migrations.RemoveField(
            model_name='calibrationdata',
            name='p_b',
        ),
        migrations.RemoveField(
            model_name='calibrationdata',
            name='p_c',
        ),
        migrations.RemoveField(
            model_name='calibrationdata',
            name='q_a',
        ),
        migrations.RemoveField(
            model_name='calibrationdata',
            name='q_b',
        ),
        migrations.RemoveField(
            model_name='calibrationdata',
            name='q_c',
        ),
        migrations.RemoveField(
            model_name='calibrationdata',
            name='voltage_a',
        ),
        migrations.RemoveField(
            model_name='calibrationdata',
            name='voltage_b',
        ),
        migrations.RemoveField(
            model_name='calibrationdata',
            name='voltage_c',
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='i1_imag_sim',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='i1_real_sim',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='p_a_downstream',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='p_a_feeder',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='p_b_downstream',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='p_b_feeder',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='p_c_downstream',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='p_c_feeder',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='q_a_downstream',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='q_a_feeder',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='q_b_downstream',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='q_b_feeder',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='q_c_downstream',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='q_c_feeder',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='v1_imag_downstream',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='v1_imag_feeder',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='v1_real_downstream',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='v1_real_feeder',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='volt_ang_a_downstream',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='volt_ang_a_feeder',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='volt_ang_b_downstream',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='volt_ang_b_feeder',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='volt_ang_c_downstream',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='volt_ang_c_feeder',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='volt_mag_a_downstream',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='volt_mag_a_feeder',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='volt_mag_b_downstream',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='volt_mag_b_feeder',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='volt_mag_c_downstream',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationdata',
            name='volt_mag_c_feeder',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
