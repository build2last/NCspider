# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='sina_article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('news_id', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('news_url', models.CharField(max_length=200)),
                ('source', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('put_time', models.DateTimeField()),
                ('content', models.TextField()),
                ('comment_url', models.CharField(max_length=250)),
                ('comments_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='sina_comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('news_id', models.CharField(max_length=100)),
                ('m_id', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=100)),
                ('comment', models.TextField()),
                ('put_time', models.DateTimeField()),
                ('parent_id', models.CharField(max_length=50)),
                ('agree_count', models.IntegerField(default=0)),
                ('against_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='sohu_article',
            fields=[
                ('news_id', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('put_time', models.DateTimeField()),
                ('comments_number', models.IntegerField()),
                ('content', models.TextField()),
                ('news_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='sohu_comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comments_id', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=50)),
                ('datetime', models.DateTimeField()),
                ('comment', models.TextField()),
                ('news', models.ForeignKey(verbose_name=b'sohu related news', to='news_opin.sohu_article')),
            ],
        ),
        migrations.CreateModel(
            name='tencent_article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('news_id', models.CharField(max_length=50)),
                ('parent_name', models.CharField(max_length=200)),
                ('news_url', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('abstract', models.CharField(max_length=200)),
                ('source', models.CharField(max_length=50)),
                ('time', models.DateTimeField(verbose_name='')),
                ('content', models.TextField()),
                ('comments_id', models.CharField(max_length=60)),
                ('comments_url', models.CharField(max_length=200)),
                ('comments_number', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-time'],
                'verbose_name': '\u6807\u9898',
            },
        ),
        migrations.CreateModel(
            name='tencent_comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('news_id', models.CharField(max_length=50)),
                ('comments_id', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=100)),
                ('comment', models.TextField()),
                ('put_time', models.DateTimeField()),
                ('sex', models.CharField(max_length=10)),
                ('reply_id', models.CharField(max_length=50)),
                ('agree_count', models.IntegerField(default=0)),
            ],
        ),
    ]
