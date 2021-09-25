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
        print(data)
        if type(data['point_to']) == str:
            data['point_to'] = list(map(float, data['point_to'].split(',')))
        elif type(data['point_to']) == list:
            data['point_to'] = data['point_to']  # todo
        if type(data['point_from']) == str:
            data['point_from'] = list(map(float, data['point_from'].split(',')))
        elif type(data['point_from']) == list:
            data['point_from'] = data['point_from']  # todo
        # data['point_to'] = list(map(float, data['point_to'].split(',')))
        # data['point_from'] = data['point_from']  # todo
        # data['point_from'] = list(map(float, data['point_from'].split(',')))
        profile = data['profile']
        # todo: new filters
        # filtered_list = self.get_restricted(data)
        # accepted_list, restricted_list = PointWrapper.filter_by_chars(filtered_list, data['user_config'])
        # print('restricted_list', restricted_list)
        # print('accepted_list', accepted_list)
        # block_area = PointWrapper.get_restricted_areas(restricted_list)
        headers = {'Authorizations': 'e4c820ba-37c0-4801-9bba-3b559cea39ab', 'content-type': 'application/json'}
        post_body = {
            'points': [data['point_from'], data['point_to']],
            "profile": profile,
            'points_encoded': False,
            'locale': 'ru',
            'ch.disable': True,
            # 'block_area': block_area
        }
        response = requests.post(url='https://graphhopper.com/api/1//route?key=e4c820ba-37c0-4801-9bba-3b559cea39ab',
                                 headers=headers, data=json.dumps(post_body))

        return Response(response.json(), status=status.HTTP_200_OK)

    # def get_restricted(self, points):
    #     points = PointWrapper.find_in_rect(points['point_from'], points['point_to'])
    #     return points
