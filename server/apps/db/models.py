from django.db import models


class Point(models.Model):
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')

    def __str__(self):
        return "{}, {}".format(str(self.lat), str(self.lon))

    class Meta:
        verbose_name = 'Точка'
        verbose_name_plural = 'Точки'


class Measure(models.Model):
    date = models.DateTimeField(verbose_name='Дата и время измерения')
    temp = models.FloatField(verbose_name='Температура')
    wet = models.FloatField(verbose_name='Влажность')
    CO2 = models.FloatField(verbose_name='Содержания CO2')
    LOS = models.FloatField(verbose_name='Значение ЛОС')
    dust_pm_1 = models.FloatField(verbose_name='Значение пыли pm 1.0')
    dust_pm_2_5 = models.FloatField(verbose_name='Значение пыли pm 2.5')
    dust_pm_10 = models.FloatField(verbose_name='Значение пыли pm 10')
    pressure = models.FloatField(verbose_name='Давление')
    AQI = models.FloatField(verbose_name='Значение AQI')
    formaldehyde = models.FloatField(verbose_name='Формальдегид')
    point = models.ForeignKey(to="Point", on_delete=models.CASCADE, verbose_name="Координаты")

    def __str__(self):
        return "[{}]: {}".format(str(self.point), str(self.date))

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
