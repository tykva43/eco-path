# Generated by Django 3.2.2 on 2021-09-16 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DisabilityRequirements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование доступного условия')),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(verbose_name='Широта')),
                ('lon', models.FloatField(verbose_name='Долгота')),
                ('type', models.CharField(choices=[('П', 'Переход'), ('З', 'Заведение')], max_length=1, verbose_name='Тип места')),
                ('characteristics', models.ManyToManyField(to='db.DisabilityRequirements', verbose_name='Характеристики места')),
            ],
        ),
        migrations.CreateModel(
            name='DisabilityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование вида недееспособности')),
                ('requirements', models.ManyToManyField(to='db.DisabilityRequirements', verbose_name='Доступные условия')),
            ],
        ),
    ]
