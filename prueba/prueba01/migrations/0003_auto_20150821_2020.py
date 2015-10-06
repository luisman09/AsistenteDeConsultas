# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prueba01', '0002_municipio'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='estado',
            options={'ordering': ['id_edo'], 'managed': False},
        ),
        migrations.AlterModelOptions(
            name='municipio',
            options={'ordering': ['id_edo', 'id_mun'], 'managed': False},
        ),
    ]
