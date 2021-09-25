import json
import random
import requests

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

        return Response(response.json(), status=status.HTTP_200_OK)

