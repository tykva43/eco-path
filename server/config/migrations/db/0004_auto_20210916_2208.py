# Generated by Django 3.2.2 on 2021-09-16 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_alter_point_characteristics'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='disabilityrequirement',
            options={'verbose_name': 'Характеристика точки', 'verbose_name_plural': 'Характеристики точек'},
        ),
        migrations.AlterModelOptions(
            name='disabilitytype',
            options={'verbose_name': 'Вид недееспособности', 'verbose_name_plural': 'Виды недееспособностей'},
        ),
        migrations.AlterModelOptions(
            name='point',
            options={'verbose_name': 'Точка', 'verbose_name_plural': 'Точки'},
        ),
    ]
