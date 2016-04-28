# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_opin', '0002_auto_20160219_0245'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tencent_article',
            options={'ordering': ['-put_time'], 'verbose_name': '\u817e\u8baf'},
        ),
        migrations.RenameField(
            model_name='sina_article',
            old_name='comment_url',
            new_name='comments_url',
        ),
        migrations.RenameField(
            model_name='tencent_article',
            old_name='time',
            new_name='put_time',
        ),
    ]
