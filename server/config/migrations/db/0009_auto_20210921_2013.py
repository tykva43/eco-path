# Generated by Django 3.2.2 on 2021-09-21 17:13

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0008_alter_peopletype_requirements'),
    ]

    operations = [
        migrations.RenameField(
            model_name='point',
            old_name='type',
            new_name='point_type',
        ),
        migrations.AlterField(
            model_name='peopletype',
            name='requirements',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None, verbose_name='Доступные условия'),
        ),
        migrations.AlterField(
            model_name='point',
            name='characteristics',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, null=True, size=None, verbose_name='Характеристики места'),
        ),
    ]
