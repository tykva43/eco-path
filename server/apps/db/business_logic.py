from apps.db.models import Measure, Point


class PointWrapper:
    @staticmethod
    def save(data):
        point = Point(
            lat=data['lat'],
            lon=data['lon'],
        )
        point.save()
        return point

    @staticmethod
    def bulk_create(data):
        points = [Point(
            lat=point['lat'],
            lon=point['lon'],
        ) for point in data]
        Point.objects.bulk_create(points)

    @staticmethod
    def find_by_coords(lat, lon):
        point = Point.objects.filter(lat=lat, lon=lon).first()
        return point

    @staticmethod
    def clear():
        Point.objects.all().delete()


class MeasureWrapper:
    @staticmethod
    def save(data):
        point = PointWrapper.find_by_coords(data['lat'], data['lon'])
        measure = Measure(
            point=point,
            date=data['date'],
            temp=data['temp'],
            wet=data['wet'],
            CO2=data['CO2'],
            LOS=data['LOS'],
            dust_pm_1=data['dust_pm_1'],
            dust_pm_2_5=data['dust_pm_2_5'],
            dust_pm_10=data['dust_pm_10'],
            pressure=data['pressure'],
            AQI=data['AQI'],
            formaldehyde=data['formaldehyde']
        )
        measure.save()
        return measure

    @staticmethod
    def bulk_create(data):
        print('batch started')
        batch = (Measure(
                point=PointWrapper.find_by_coords(b['lat'], b['lon']),
                date=b['date'],
                temp=b['temp'],
                wet=b['wet'],
                CO2=b['CO2'],
                LOS=b['LOS'],
                dust_pm_1=b['dust_pm_1'],
                dust_pm_2_5=b['dust_pm_2_5'],
                dust_pm_10=b['dust_pm_10'],
                pressure=b['pressure'],
                AQI=b['AQI'],
                formaldehyde=b['formaldehyde']
        )
                for b in data)
        Measure.objects.bulk_create(batch)
        print('batch  completed')

    @staticmethod
    def clear():
        Measure.objects.all().delete()
