# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id_edo', models.IntegerField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'estado',
                'managed': False,
            },
        ),
    ]
