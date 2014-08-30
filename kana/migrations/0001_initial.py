# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='base_kana',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('kana', models.CharField(max_length=2)),
                ('unicode', models.CharField(blank=True, max_length=20, null=True)),
                ('pronunciation', models.CharField(max_length=5)),
                ('pronunciation_tip', models.CharField(blank=True, max_length=50, null=True)),
                ('mnemonic', models.CharField(blank=True, max_length=200, null=True)),
                ('comment', models.CharField(blank=True, max_length=200, null=True)),
                ('vowel_group', models.CharField(blank=True, max_length=5, null=True)),
                ('consonant_group', models.CharField(blank=True, max_length=5, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='derived_kana',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('kana', models.CharField(max_length=2)),
                ('unicode', models.CharField(blank=True, max_length=20, null=True)),
                ('pronunciation', models.CharField(max_length=5)),
                ('pronunciation_tip', models.CharField(blank=True, max_length=50, null=True)),
                ('comment', models.CharField(blank=True, max_length=200, null=True)),
                ('vowel_group', models.CharField(blank=True, max_length=5, null=True)),
                ('consonant_group', models.CharField(blank=True, max_length=5, null=True)),
                ('base_kana_id', models.ForeignKey(to='kana.base_kana')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
