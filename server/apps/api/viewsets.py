import json
import requests
from django.db.models import F

from django.http import QueryDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.db.models import Measure, Point


class PointView(APIView):
    def get(self, request):
        queryset = Point.objects.all().values()
        all_points = {'type': 'FeatureCollection',
                      'features': [{'type': 'Feature',
                                    'properties': {'value': point['value']/200},
                                    'geometry': {
                                        'type': 'Point',
                                        'coordinates': [point['lon'], point['lat']]
                                    }} for point in queryset]}
        return Response(all_points)


class RouterBuilder(APIView):
    def post(self, request):
        data = request.data
        # preprocess points data
        data = QueryDict.dict(data)
        if type(data['point_to']) == str:
            data['point_to'] = list(map(float, data['point_to'].split(',')))
        elif type(data['point_to']) == list:
            data['point_to'] = data['point_to']
        if type(data['point_from']) == str:
            data['point_from'] = list(map(float, data['point_from'].split(',')))
        elif type(data['point_from']) == list:
            data['point_from'] = data['point_from']
        profile = data['profile']
        headers = {'Authorizations': 'e4c820ba-37c0-4801-9bba-3b559cea39ab', 'content-type': 'application/json'}
        post_body = {
            'points': [data['point_from'], data['point_to']],
            "profile": profile,
            'points_encoded': False,
            'locale': 'ru',
            # 'ch.disable': True,
            'algorithm': 'alternative_route',
            'alternative_route.max_paths': 5,
            'alternative_route.max_weight_factor': 3,
        }
        response = requests.post(url='https://graphhopper.com/api/1//route?key=e4c820ba-37c0-4801-9bba-3b559cea39ab',
                                 headers=headers, data=json.dumps(post_body))

        resp_copy = response.json()
        print(resp_copy.keys())
        if 'paths' not in resp_copy.keys():
            return Response(resp_copy, status=status.HTTP_400_BAD_REQUEST)

        f = lambda x, y: min(x, y) + abs(x - y) / 2
        pow2 = lambda x: x * x
        eco_coeffs = []

        for path in resp_copy['paths']:
            values_in_point = []
            for i in range(len(path['points']['coordinates'])-1):
                point_a = path['points']['coordinates'][i]
                point_b = path['points']['coordinates'][i+1]
                center = [f(point_a[0], point_b[0]), f(point_a[1], point_b[1])]
                # Находим треугольник, который описывает выбранную точку пути
                points = Point.objects.all().annotate(distance=(pow2(center[0]-F('lon'))+pow2(center[1]-F('lat')))**0.5).order_by('distance')[:3]

                # # Строим уравнение плоскости по трем точкам (lat as x, lon as y, AQI value as z)
                point1 = points[0]
                point2 = points[1]
                point3 = points[2]

                a1 = (point2.lat - point1.lat)
                b1 = (point2.lon - point1.lon)
                c1 = point2.value - point1.value

                a2 = 1 * (point3.lat - point1.lat)
                b2 = 1 * (point3.lon - point1.lon)
                c2 = point3.value - point1.value

                # Уравнение плоскости
                a = b1 * c2 - b2 * c1
                b = a2 * c1 - a1 * c2
                c = a1 * b2 - b1 * a2
                d = (- a * point1.lat - b * point1.lon - c * point1.value)

                # Отсюда value = (-d - a*lat - b*lon)/c
                # Значение AQI в текущей точке середины отрезка пути
                try:
                    values_in_point.append((-d - a*center[0] - b*center[1])/c)
                except ZeroDivisionError:
                    values_in_point.append(100.0)

                # print(values_in_point)
            eco_coeffs.append(sum(values_in_point)/len(values_in_point))
        print('eco_coeffs', eco_coeffs, 'min', min(eco_coeffs), 'min_i', eco_coeffs.index(min(eco_coeffs)))
        index_min_path = eco_coeffs.index(min(eco_coeffs))
        optimal_path = resp_copy['paths'].pop(index_min_path)
        resp_copy['paths'] = optimal_path
        return Response(resp_copy, status=status.HTTP_200_OK)
