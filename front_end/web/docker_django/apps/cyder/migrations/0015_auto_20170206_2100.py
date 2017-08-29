# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyder', '0014_auto_20170206_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermodel',
            old_name='simulation_date',
            new_name='last_modified',
        ),
    ]
