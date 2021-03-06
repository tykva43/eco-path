# Generated by Django 3.2.2 on 2021-09-25 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0010_auto_20210925_0829'),
    ]

    operations = [
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(verbose_name='Широта')),
                ('lon', models.FloatField(verbose_name='Долгота')),
            ],
        ),
        migrations.RemoveField(
            model_name='measure',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='measure',
            name='lon',
        ),
        migrations.AddField(
            model_name='measure',
            name='point',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='db.point', verbose_name='Координаты'),
            preserve_default=False,
        ),
    ]
