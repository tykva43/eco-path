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


class MeasureWrapper:
    @staticmethod
    def save(data):
        point = PointWrapper.find_by_coords(data['lat'], data['lon'])
        measure = Measure(
            point__id=point.id,
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


# class MeasureWrapper:
#     @staticmethod
#     def save(data):
#         point = Point(
#             lat=data['lat'],
#             lon=data['lon'],
#             point_type=data['point_type'],
#             characteristics=data['characteristics']
#         )
#         point.save()
#
#     @staticmethod
#     def bulk_save(data):
#         batch = [Point(lat=row['lat'],
#                        lon=row['lon'],
#                        point_type=row['point_type'],
#                        characteristics=str(row['characteristics']).split(','))
#                  for row in data]
#         Point.objects.bulk_create(batch)
#
#     @staticmethod
#     def all():
#         return Point.objects.all()
#
#     @staticmethod
#     def clear_all():
#         Point.objects.all().delete()
#
#     @staticmethod
#     def find_by_lon_and_lat(lon: str, lat: str):
#         return Point.objects.filter(lon=lon, lat=lat)
#
#     @staticmethod
#     def find_in_rect(point_a, point_b):
#         min_lon = min(point_b[0], point_a[0])
#         max_lon = max(point_b[0], point_a[0])
#         min_lat = min(point_b[1], point_a[1])
#         max_lat = max(point_b[1], point_a[1])
#         return Point.objects.filter(lon__lte=max_lon, lon__gte=min_lon, lat__lte=max_lat, lat__gte=min_lat)
#
#     @staticmethod
#     def filter_by_chars(queryset, p_type_id):
#         p = PeopleTypeWrapper.find_by_id(p_type_id)
#         reqs = set(p.requirements)
#         dict_data = queryset.values()
#         accepted = [d for d in dict_data if reqs.issubset(d['characteristics'])]
#         restricted = [d for d in dict_data if not reqs.issubset(d['characteristics'])]
#         return accepted, restricted
#
#     @staticmethod
#     def get_restricted_areas(restricted):
#         LEN = 25
#         circles = ''
#         for r in restricted:
#             circles += '{},{},{};'.format(str(r['lat']), str(r['lon']), str(LEN))
#         print(circles)
#
#         return circles[:-1]
