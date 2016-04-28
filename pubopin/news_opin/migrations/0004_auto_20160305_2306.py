# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_opin', '0003_auto_20160305_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sina_comment',
            name='m_id',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='sina_comment',
            name='parent_id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tencent_article',
            name='comments_id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tencent_article',
            name='news_id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tencent_comment',
            name='comments_id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tencent_comment',
            name='news_id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tencent_comment',
            name='reply_id',
            field=models.CharField(max_length=100),
        ),
    ]
