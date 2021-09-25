import json
import random
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
                                    'properties': {'value': random.random()},
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
            'ch.disable': True,
            'algorithm': 'alternative_route',
            'alternative_route.max_paths': 5,
        }
        response = requests.post(url='https://graphhopper.com/api/1//route?key=e4c820ba-37c0-4801-9bba-3b559cea39ab',
                                 headers=headers, data=json.dumps(post_body))

        resp_copy = response.json()
        # print(resp_copy)
        # print("resp_copy['paths']", resp_copy['paths'])
        # print('len', len(resp_copy['paths']))
        eco_coeffs = []
        for path in resp_copy['paths']:
            for i in range(len(path['points']['coordinates'])-1):
                point_a = path['points']['coordinates'][i]
                point_b = path['points']['coordinates'][i+1]
                f = lambda x, y: min(x, y) + abs(x-y)/2
                p2 = lambda x: x*x
                center = [f(point_a[0], point_b[0]), f(point_a[1], point_b[1])]
                points = Point.objects.all().annotate(distance=(p2(center[0]-F('lon'))+p2(center[1]-F('lat')))**0.5).order_by('distance')

                # print(points)
                # print('point_a', point_a)
                # print('point_b', point_b)
                # print('center', center)
                # print()
                ...

        return Response(response.json(), status=status.HTTP_200_OK)

