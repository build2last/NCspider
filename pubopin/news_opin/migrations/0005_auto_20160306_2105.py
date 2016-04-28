# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_opin', '0004_auto_20160305_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sina_comment',
            name='m_id',
            field=models.CharField(unique=True, max_length=200),
        ),
    ]
