# Generated by Django 3.2.2 on 2021-09-25 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0012_alter_point_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='value',
            field=models.FloatField(default=0.0, verbose_name='Значение ИЗА'),
        ),
    ]
