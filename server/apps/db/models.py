from django.db import models


class Point(models.Model):
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    value = models.FloatField(verbose_name='Значение ИЗА', default=0.0)

    def __str__(self):
        return "{}, {}".format(str(self.lat), str(self.lon))

    class Meta:
        verbose_name = 'Точка'
        verbose_name_plural = 'Точки'


class Measure(models.Model):
    date = models.DateTimeField(verbose_name='Дата и время измерения')
    temp = models.FloatField(verbose_name='Температура', null=True, blank=True)
    wet = models.FloatField(verbose_name='Влажность', null=True, blank=True)
    CO2 = models.FloatField(verbose_name='Содержания CO2', null=True, blank=True)
    LOS = models.FloatField(verbose_name='Значение ЛОС', null=True, blank=True)
    dust_pm_1 = models.FloatField(verbose_name='Значение пыли pm 1.0', null=True, blank=True)
    dust_pm_2_5 = models.FloatField(verbose_name='Значение пыли pm 2.5', null=True, blank=True)
    dust_pm_10 = models.FloatField(verbose_name='Значение пыли pm 10', null=True, blank=True)
    pressure = models.FloatField(verbose_name='Давление', null=True, blank=True)
    AQI = models.FloatField(verbose_name='Значение AQI', null=True, blank=True)
    formaldehyde = models.FloatField(verbose_name='Формальдегид', null=True, blank=True)
    point = models.ForeignKey(to="Point", on_delete=models.CASCADE, verbose_name="Координаты")

    def __str__(self):
        return "[{}]: {}".format(str(self.point), str(self.date))

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
