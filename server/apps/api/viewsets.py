import json
import math
import requests

from django.http import QueryDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.db.models import Measure


# class PointView(APIView):
#     def get(self, request):
#         if request.GET:
#             data = QueryDict.dict(request.GET)
#             queryset = Point.objects.all()
#             accepted_list, restricted_list = PointWrapper.filter_by_chars(queryset, data['user_config'])
#             features = []
#             for e in accepted_list:
#                 features.append(
#                     {'type': 'Feature',
#                      'properties': {'characteristics': [] if math.isnan(e['characteristics'][0])
#                      else map(int, e['characteristics']), 'is_accepted': True},
#                      'geometry': {
#                          'type': 'Point',
#                          'coordinates': [e['lon'], e['lat']]
#                      }}
#                 )
#             for e in restricted_list:
#                 features.append(
#                     {'type': 'Feature',
#                      'properties': {'characteristics': [] if math.isnan(e['characteristics'][0])
#                      else map(int, e['characteristics']), 'is_accepted': False},
#                      'geometry': {
#                          'type': 'Point',
#                          'coordinates': [e['lon'], e['lat']]
#                      }}
#                 )
#             all_points = {'type': 'FeatureCollection',
#                           'features': features}
#             return Response(all_points)
#
#         else:
#             queryset = Point.objects.all().values()
#             all_points = {'type': 'FeatureCollection',
#                           'features': [{'type': 'Feature',
#                                         'properties': {'characteristics': [] if math.isnan(point['characteristics'][0])
#                                         else map(int, point['characteristics'])},
#                                         'geometry': {
#                                             'type': 'Point',
#                                             'coordinates': [point['lon'], point['lat']]
#                                         }} for point in queryset]}
#             return Response(all_points)


class RouterBuilder(APIView):
    def post(self, request):
        data = request.data
        # preprocess points data
        data = QueryDict.dict(data)
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
        # print(data['point_from'])
        # params = {
        #     'point': ','.join(map(str, data['point_from'])),
        #           'point': ','.join(map(str, data['point_to'])),
        #     #       'point': data['point_from'],
        #     #       'point': data['point_to'],
        #           "vehicle": "foot",
        #           'calc_points': True,
        #           'locale': 'ru',
        #           'key': 'e4c820ba-37c0-4801-9bba-3b559cea39ab',
        #           }
        post_body = {
            'points': [data['point_from'], data['point_to']],
            "profile": profile,
            'points_encoded': False,
            'locale': 'ru',
            'ch.disable': True,
            # 'block_area': block_area
        }
        # response = requests.post(url='https://graphhopper.com/api/1//route?point={},{}&point={},{}&vehicle=foot&calc_points=true&locale=ru&key=e4c820ba-37c0-4801-9bba-3b559cea39ab'.format(data['point_from'][1], data['point_from'][0], data['point_to'][1], data['point_to'][0]), headers=headers)
        response = requests.post(url='https://graphhopper.com/api/1//route?key=e4c820ba-37c0-4801-9bba-3b559cea39ab',
                                 headers=headers, data=json.dumps(post_body))
        # print(response.json())
        # print(response.url)
        # post_data = {'name': 'Gladys'}
        # response = requests.post('http://example.com', data=post_data)
        # content = response.content

        # print(restricted_list)

        return Response(response.json(), status=status.HTTP_200_OK)

    def get_restricted(self, points):
        points = PointWrapper.find_in_rect(points['point_from'], points['point_to'])
        return points
