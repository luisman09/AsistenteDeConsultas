# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prueba01', '0005_auto_20150825_1456'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='estado',
            options={'ordering': ['id'], 'managed': False},
        ),
    ]
