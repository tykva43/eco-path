from django.urls import path
from rest_framework import routers

# from apps.api.viewsets import UserViewSet #, PointViewSet
from apps.analysis.build_data import collect_from_dir
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .viewsets import RouterBuilder

app_name = 'api'

# router = routers.SimpleRouter()
# router.register(r'user', UserViewSet, basename='User')
# router.register(r'points', PointViewSet, basename='Point')
# urlpatterns = router.urls
urlpatterns = []

@api_view(('GET', 'POST',))
def test(req):
    return Response({'info': 'ok'})

urlpatterns += [
    path('points/', collect_from_dir),
    path('get_route/', RouterBuilder.as_view()),
    path('test/', test)
    # path('get_people_types/', PeopleTypeView.as_view({'get': 'list'})),
    # path('get_chars/', DisabilityRequirementViewSet.as_view({'get': 'list'})),
]
