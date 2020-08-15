from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework import renderers
from rest_framework.decorators import action
# from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers as django_core_serializers
from django.http import HttpResponse, JsonResponse

from first_api import serializers 
from first_api import models
from first_api import permission
import json

## helper function

def notFoundHandling(result,error_message="Not found."):
    if(len(result)>0):
        return Response(result)
    else: 
        return Response({ "detail": error_message},
        status=status.HTTP_404_NOT_FOUND)

class VillagesZonesService(viewsets.ModelViewSet):
    serializer_class = serializers.HomeSerializer
    queryset = models.Village.objects.filter(is_active=True)
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(detail=True, methods = 'GET')
    def get_villages_zones(self, request):
        """ eturn all village and all zone correspond to its."""

        result_list = []

        villageQuerySet = models.Village.objects.all()
        villageSerializer = serializers.VillageSerializer(villageQuerySet,many=True)
        villageData = villageSerializer.data

        for village in villageData:
            village_dict = dict()
            village_dict["pk"] = village["pk"]
            village_dict["village_name"] = village["village_name"]

            zone_list = []
            zoneQuerySet = models.Zone.objects.filter(zone_village=village_dict["pk"]).all()
            zoneSerializer = serializers.ZoneSerializer(zoneQuerySet,many=True)
            zoneData = zoneSerializer.data
            
            for zone in zoneData:
                zone_dict = dict()
                zone_dict["pk"] = zone["pk"]
                zone_dict["zone_name"] = zone["zone_name"]
                zone_dict["zone_number"] = zone["zone_number"]   
                zone_list.append(zone_dict)

            village_dict['zone'] = zone_list
            result_list.append(village_dict)

        return notFoundHandling(result_list)

