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
import datetime
from django.db.models import Count
from django.db.models import Sum

from django.conf import settings
from django.utils.timezone import make_aware
from django.utils.timezone import localtime, now

## helper function

def notFoundHandling(result,error_message="Not found."):
    if(len(result)>0):
        return Response(result)
    else: 
        return Response({ "detail": error_message},
        status=status.HTTP_404_NOT_FOUND)


## User views

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profile"""
    serializer_class = serializers.UserProfileSerializer
    ## contains the standard CRUD operation of View Set such list, create ...
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,permission.UpdateOwnProfile,)

    @action(detail=True, methods = 'GET')
    def get_profiles_check(self, request, new_username):
        """ Return all active company"""
        querySet = models.UserProfile.objects.filter(username=new_username)
        serializer = serializers.UserProfileSerializer(querySet,many=True)
        result = serializer.data

        if(len(result)>0):
            return Response({ "detail": 'duplicate username'},
                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail':'useable username'})

    
    @action(detail=True, methods = 'GET')
    def get_profiles_detail(self, request, username):
        """ Return their own profile according to username"""
        querySet = models.UserProfile.objects.filter(username=username).last()
        serializer = serializers.UserProfileSerializer(querySet)
        result = serializer.data
        
        result.pop('groups', None)

        if(result['user_role']=='SecureBoss' or result['user_role']=='SecureGuard'):
            usernamePk = result['pk']
            username = models.UserProfile.objects.only('pk').get(pk=usernamePk)
            secure = models.SecureGuard.objects.filter(secure_username=username).last()
            serializer = serializers.SecureGuardSerializer(secure)
            secureData = serializer.data
        
            secureDict = dict()
            secureDict["pk"] = secureData["pk"]
            secureDict["secure_firstname"] = secureData["secure_firstname"]
            secureDict["secure_lastname"]= secureData["secure_lastname"]
            secureDict["secure_username"]= secureData["secure_username"]
            secureDict["secure_type"]= secureData["secure_type"]
            secureDict["secure_zone"]= secureData["secure_zone"]
            secureDict["secure_village"]= secureData["secure_village"]
            secureDict["secure_company"]= secureData["secure_company"]

            result['secure_guard'] = secureDict

        elif(result['user_role']=='GeneralUser'):
            usernamePk = result['pk']
            username = models.UserProfile.objects.only('pk').get(pk=usernamePk)
            genuser = models.GeneralUser.objects.filter(gen_user_username=username).last()
            serializer = serializers.GeneralUserSerializer(genuser)
            genUserData = serializer.data
            genUserData.pop('is_active', None)

            result['general_user'] = genUserData



        return notFoundHandling(result)
        

# Home Secure main views 

class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = models.Company.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods = 'GET')
    def get_companys_active(self, request):
        """ Return all active company"""
        querySet = models.Company.objects.filter(is_active=True)
        serializer = serializers.CompanySerializer(querySet,many=True)
        result = serializer.data

        return notFoundHandling(result)
    
class VillageViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VillageSerializer
    queryset = models.Village.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['post'])
    def create_village_with_setting(self, request):
        """ Create qr code from user incase report the vehicle which not have enter history"""
        data = request.data
        isExist = models.Company.objects.filter(pk=data['village_company']).exists()
        if(isExist==False):
            return Response({ "detail": "Not found company."},status=status.HTTP_404_NOT_FOUND)
        else:
            company = models.Company.objects.only('pk').get(pk=data['village_company'])

       
        village = models.Village.objects.create(village_name=data['village_name'], village_address=data['village_address'],village_company=company,village_lat=data['village_lat'],village_lon=data['village_lon'])
        village.save
        serializer = serializers.VillageSerializer(village)

        setting = models.Setting.objects.create(setting_village=village)
        setting.save


        return Response(serializer.data,status.HTTP_201_CREATED)

    @action(detail=True, methods = 'GET')
    def get_villages_active(self, request):
        """ Return all active village"""
        querySet = models.Village.objects.filter(is_active=True)
        serializer = serializers.VillageSerializer(querySet,many=True)
        result = serializer.data

        return notFoundHandling(result)
    
    @action(detail=True, methods = 'GET')
    def get_companys_pk_villages(self, request, pk):
        """ Return all village to specific company"""
        querySet = models.Village.objects.filter(village_company=pk).all()
        serializer = serializers.VillageSerializer(querySet,many=True)
        result = serializer.data
        
        return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def get_villages_location_pk(self, request, villagePk):
        """ Return location of specific village"""
        querySet = models.Village.objects.filter(is_active=True, pk = villagePk).all()
        serializer = serializers.VillageSerializer(querySet,many=True)
        villageData = serializer.data


        final = []
        
        for village in villageData:
            village_dict = dict()
            village_dict["pk"] = village["pk"]
            village_dict['village_lat'] = village['village_lat']
            village_dict['village_lon'] = village['village_lon']

            final.append(village_dict)
        
        if(len(final)<1 ):
            return Response({ "detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
        if(len(final)>1 ):
            return Response({ "detail": "Error, multiple home"},status=status.HTTP_404_NOT_FOUND)
       
        return notFoundHandling(final[0])



 # renderer_classes = [renderers.JSONRenderer] add thuis if need only json 

    
class ZoneViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ZoneSerializer
    queryset = models.Zone.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods = 'GET')
    def get_companys_pk_villages_zones(self, request, company_pk):
        """ Return all zone according to all village, filter by company pkNote: get only active village """
        
        result_list = []

        villageQuerySet = models.Village.objects.filter(village_company=company_pk,is_active=True).all()
        villageSerializer = serializers.VillageSerializer(villageQuerySet,many=True)
        villageData = villageSerializer.data

        for village in villageData:
            village_dict = dict()
            village_dict["pk"] = village["pk"]
            village_dict["village_name"] = village["village_name"]

            zone_list = []
            zoneQuerySet = models.Zone.objects.filter(zone_village=village_dict["pk"],is_active=True).all()
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

    @action(detail=True, methods = 'GET')
    def get_villages_zones(self, request):
        """ Return all zone according to all village, Note: get only active village """
        
        result_list = []

        villageQuerySet = models.Village.objects.filter(is_active=True).all()
        villageSerializer = serializers.VillageSerializer(villageQuerySet,many=True)
        villageData = villageSerializer.data

        for village in villageData:
            village_dict = dict()
            village_dict["pk"] = village["pk"]
            village_dict["village_name"] = village["village_name"]

            zone_list = []
            zoneQuerySet = models.Zone.objects.filter(zone_village=village_dict["pk"],is_active=True).all()
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

    @action(detail=True, methods = 'GET')
    def get_villages_pk_zones(self, request, pk):
        """ Return all zone to specific village"""
        querySet = models.Zone.objects.filter(zone_village=pk).all()
        serializer = serializers.ZoneSerializer(querySet,many=True)
        result = serializer.data
        
        return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def get_villages_pk_zones_pk(self, request, village_pk, zone_pk ):
        """ Return specific zone to specific village"""
        querySet = models.Zone.objects.filter(zone_village=village_pk, pk=zone_pk).all()
        serializer = serializers.ZoneSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)


    

    # @action(detail=True, methods = 'GET', renderer_classes=[renderers.JSONRenderer])
    # def zone_by_village(self, request, pk):
    #     """Return all zone according to that village id, pk is village_id"""
    #     zone_by_village = list(models.Zone.objects.filter(zone_village = pk).values())
        
    #     if(len(zone_by_village)>0):
    #         return Response(zone_by_village)
    #     else:
    #         ## not found specific village
    #         return Response(
    #             { "detail": "Not found."},
    #             status=status.HTTP_404_NOT_FOUND
    #         )


## use only post from home 
class HomeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HomeSerializer
    # queryset = models.Home.objects.filter(is_active=True)
    queryset = models.Home.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods = 'GET')
    def get_homes_pk_homenumber(self, request, home_pk):
        """ Return pk and home_number of homes according to request homePk"""
        isExist = models.Home.objects.filter(pk=home_pk, is_active=True).exists()
        if(isExist==False):
            return Response({ "detail": "Not have this home number"},status=status.HTTP_404_NOT_FOUND)
        else:
            querySet = models.Home.objects.filter(pk=home_pk, is_active=True).last()
            serializer = serializers.HomeSerializer(querySet)
            result = serializer.data
            # print(result)
            
            return Response({"home_number":result['home_number']})


    @action(detail=True, methods = 'GET')
    def get_homespk_number(self, request, home_number):
        """ Return pk and home_number of homes according to request homeNumber"""
        isExist = models.Home.objects.filter(home_number=home_number, is_active=True).exists()
        if(isExist==False):
            return Response({ "detail": "Not have this home number"},status=status.HTTP_404_NOT_FOUND)
        else:
            querySet = models.Home.objects.filter(home_number=home_number, is_active=True).last()
            serializer = serializers.HomeSerializer(querySet)
            result = serializer.data
            # print(result)
            
            return Response({"pk":result['pk'],"home_number":result['home_number']})
    

    @action(detail=True, methods = 'GET')
    def get_homes_number(self, request, number):
        """ Return all homes filtered by home_number """
        querySet = models.Home.objects.filter(home_number=number, is_active=True).all()
        serializer = serializers.HomeSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)


    @action(detail=True, methods = 'GET')
    def get_homes_active(self, request):
        """ Return all active home"""
        querySet = models.Home.objects.filter(is_active=True).all()
        serializer = serializers.HomeSerializer(querySet,many=True)
        result = serializer.data

        return notFoundHandling(result)


    @action(detail=True, methods = 'GET')
    def get_villages_pk_homes(self, request, village_pk):
        """ Return all homes correspond to specific village """
        querySet = models.Home.objects.filter(home_village=village_pk, is_active=True).all()
        serializer = serializers.HomeSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def get_villages_pk_zones_null_homes(self, request, village_pk):
        """ Return all homes correspond to specific zone and correspond to specific village """
        querySet = models.Home.objects.filter(home_village=village_pk, is_active=True).all()
        serializer = serializers.HomeSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def get_villages_pk_zones_pk_homes(self, request, village_pk, zone_pk):
        """ Return all homes correspond to specific zone and correspond to specific village """
        querySet = models.Home.objects.filter(home_village=village_pk, home_zone=zone_pk, is_active=True).all()
        serializer = serializers.HomeSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)


    @action(detail=True, methods = 'GET')
    def get_villages_zones_homes(self, request):
        """ Return all homes correspond to each zone corespond to each village """
        querySet = models.Zone.objects.filter(zone_village=village_pk, pk=zone_pk).all()
        serializer = serializers.ZoneSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)

        # querySet = models.Home.objects.all().values()
        # result = list(querySet)        

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

                home_list = []
                homeQuerySet = models.Home.objects.filter(home_zone=zone_dict["pk"]).all()
                homeSerializer = serializers.HomeSerializer(homeQuerySet,many=True)
                homeData = homeSerializer.data
                
                for home in homeData:
                    home_dict = dict()
                    home_dict["pk"] = home["pk"]
                    home_dict["home_number"] = home["home_number"]
                    home_dict["home_address"] = home["home_address"]
                    home_dict["home_zone"] = home["home_zone"]
                    home_dict["home_lat"] = home["home_lat"]
                    home_dict["home_lon"] = home["home_lon"]
                    home_dict["is_active"] = ["is_active"]
                    home_list.append(home_dict)

                zone_dict['home'] = home_list      
                zone_list.append(zone_dict)

            village_dict['zone'] = zone_list
            result_list.append(village_dict)

        ##workkk
        # querySet = models.Home.objects.all()
        # serializer = serializers.HomeSerializer(querySet,many=True)
        # result = serializer.data
        ##workkk


        # return Response(temp_list)
        return notFoundHandling(result_list)



## use only post from home 
class GeneralUserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GeneralUserSerializer
    queryset = models.GeneralUser.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods = 'GET')
    def get_general_users_active(self, request):
        """ Return all active home"""
        querySet = models.GeneralUser.objects.filter(is_active=True).all()
        serializer = serializers.GeneralUserSerializer(querySet,many=True)
        result = serializer.data

        return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def get_villages_pk_general_users(self, request, village_pk):
        """ Return all homes correspond to specific zone and correspond to specific village """
        querySet = models.GeneralUser.objects.filter(gen_user_village=village_pk, is_active=True).all()
        serializer = serializers.GeneralUserSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def get_villages_pk_zones_pk_general_users(self, request, village_pk, zone_pk):
        """ Return all homes correspond to specific zone and correspond to specific village """
        querySet = models.GeneralUser.objects.filter(gen_user_village=village_pk, gen_user_zone=zone_pk, is_active=True).all()
        serializer = serializers.GeneralUserSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)


class CheckpointViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CheckpointSerializer
    queryset = models.Checkpoint.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods = 'GET')
    def get_villages_pk_checkpoints(self, request, village_pk):
        """ Return all checkpoints correspond to specific village """
        querySet = models.Checkpoint.objects.filter(point_village=village_pk, is_active=True).all()
        serializer = serializers.CheckpointSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def get_villages_pk_zones_pk_checkpoints(self, request, village_pk, zone_pk):
        """ Return all checkpoints correspond to specific zone and correspond to specific village """
        querySet = models.Checkpoint.objects.filter(point_village=village_pk, point_zone=zone_pk, is_active=True).all()
        serializer = serializers.CheckpointSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)

class CheckinCheckpointViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CheckinCheckpointSerializer
    queryset = models.CheckinCheckpoint.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    @action(detail=True, methods = 'GET')
    def get_villages_pk_checkincheckpoints(self, request, village_pk):
        """ Return all checkpoints correspond to specific village """
        # print("get here")
        # print(village_pk)
        village = models.Village.objects.only('pk').get(pk=village_pk)
        
        querySet = models.CheckinCheckpoint.objects.filter(point_village=village, is_active=True).all()
        print(querySet)
        # for q in querySet:
        #     print(q)
        serializer = serializers.CheckinCheckpointSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)

class WorkViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WorkSerializer
    queryset = models.Work.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods = 'GET')
    def get_villages_pk_works(self, request, pk):
        """ Return all work to specific village"""
        querySet = models.Work.objects.filter(work_village=pk).all()
        serializer = serializers.WorkSerializer(querySet,many=True)
        result = serializer.data
        
        return notFoundHandling(result)

    

class SecureGuardViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SecureGuardSerializer
    queryset = models.SecureGuard.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods = 'GET')
    def get_villages_pk_secureguards(self, request, village_pk):
        """ Return all secureguards correspond to specific village """
        querySet = models.SecureGuard.objects.filter(secure_village=village_pk, is_active=True).all()
        serializer = serializers.SecureGuardSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)
    
    @action(detail=True, methods = 'GET')
    def get_villages_pk_zones_pk_secureguards(self, request, village_pk, zone_pk):
        """ Return all checkpoints correspond to specific zone and correspond to specific village """
        querySet = models.SecureGuard.objects.filter(secure_village=village_pk, secure_zone=zone_pk, is_active=True).all()
        serializer = serializers.SecureGuardSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def get_villages_pk_secureguards_for_location(self, request, village_pk):
        """ Return all secureguards correspond to specific village for selecting screen """
        querySet = models.SecureGuard.objects.filter(secure_village=village_pk, is_active=True).all()
        serializer = serializers.SecureGuardSerializer(querySet,many=True)
        secureGuardData = serializer.data

        result = []
        for secure in secureGuardData:
            secureDict = dict()
            secureDict['pk'] = secure['pk']
            secureDict['secure_firstname'] = secure['secure_firstname']
            secureDict['secure_lastname'] = secure['secure_lastname']
            secureDict['secure_type'] = secure['secure_type']
            secureDict['secure_village'] = secure['secure_village']
            secureDict['secure_zone'] = secure['secure_zone']

            # secureDict['secure_now_latitude'] = secure['secure_now_latitude']
            # secureDict['secure_now_lontitude'] = secure['secure_now_lontitude']
            # secureDict['secure_now_lontitude'] = secure['secure_now_lontitude']
            # secureDict['secure_now_location_time'] = secureDict['secure_now_location_time']

            workPk = secure['secure_work_shift']
            
            work = models.Work.objects.filter(pk=workPk, is_active=True).last()
            serializer = serializers.WorkSerializer(work)
            workData = serializer.data
            secureDict['secure_work_shift'] = secure['secure_work_shift']
            secureDict['secure_work_name'] = workData['work_name']
            result.append(secureDict)

            
        return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def get_villages_pk_zones_pk_secureguards_for_location(self, request, village_pk, zone_pk):
        """ Return all secureguards correspond to specific village and zonefor selecting screen """
        querySet = models.SecureGuard.objects.filter(secure_village=village_pk, secure_zone=zone_pk, is_active=True).all()
        serializer = serializers.SecureGuardSerializer(querySet,many=True)
        secureGuardData = serializer.data

        result = []
        for secure in secureGuardData:
            secureDict = dict()
            secureDict['pk'] = secure['pk']
            secureDict['secure_firstname'] = secure['secure_firstname']
            secureDict['secure_lastname'] = secure['secure_lastname']
            secureDict['secure_type'] = secure['secure_type']
            secureDict['secure_village'] = secure['secure_village']
            secureDict['secure_zone'] = secure['secure_zone']
            
            # secureDict['secure_now_location_time'] = secureDict['secure_now_location_time']

            workPk = secure['secure_work_shift']
            
            work = models.Work.objects.filter(pk=workPk, is_active=True).last()
            serializer = serializers.WorkSerializer(work)
            workData = serializer.data
            secureDict['secure_work_shift'] = secure['secure_work_shift']
            secureDict['secure_work_name'] = workData['work_name']
            result.append(secureDict)

            
        return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def get_villages_pk_secureguards_for_mainfetching(self, request, village_pk):
        """ Return all secureguards correspond to specific village for selecting screen """
        querySet = models.SecureGuard.objects.filter(secure_village=village_pk, is_active=True).all()
        serializer = serializers.SecureGuardSerializer(querySet,many=True)
        secureGuardData = serializer.data

        result = []
        for secure in secureGuardData:
            secureDict = dict()
            secureDict['pk'] = secure['pk']
            secureDict['secure_firstname'] = secure['secure_firstname']
            secureDict['secure_lastname'] = secure['secure_lastname']
            secureDict['secure_type'] = secure['secure_type']
            secureDict['secure_village'] = secure['secure_village']
            secureDict['secure_zone'] = secure['secure_zone']
            result.append(secureDict)

        return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def get_villages_pk_zones_pk_secureguards_for_mainfetching(self, request, village_pk, zone_pk):
        """ Return all secureguards correspond to specific village and zonefor selecting screen """
        querySet = models.SecureGuard.objects.filter(secure_village=village_pk, secure_zone=zone_pk, is_active=True).all()
        serializer = serializers.SecureGuardSerializer(querySet,many=True)
        secureGuardData = serializer.data

        result = []
        for secure in secureGuardData:
            secureDict = dict()
            secureDict['pk'] = secure['pk']
            secureDict['secure_firstname'] = secure['secure_firstname']
            secureDict['secure_lastname'] = secure['secure_lastname']
            secureDict['secure_type'] = secure['secure_type']
            secureDict['secure_village'] = secure['secure_village']
            secureDict['secure_zone'] = secure['secure_zone']
            result.append(secureDict)

        return notFoundHandling(result)

    

class SecureLocationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SecureLocationSerializer
    queryset = models.SecureLocation.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods = 'GET')
    def get_secureguards_pk_securelocation(self, request, secure_guard_pk):
        """ Return all secure location correspond to specific secure guard and also delete old set  """
       
        delQuerySet = models.SecureLocation.objects.filter(secure_location_time__lt=datetime.date.today()).all().delete()
        querySet = models.SecureLocation.objects.filter(secure_pk=secure_guard_pk).order_by('secure_location_time').all()[::-1]
        serializer = serializers.SecureLocationSerializer(querySet,many=True)
        result = serializer.data

        return notFoundHandling(result)

class SecureWorkViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SecureWorkSerializer
    queryset = models.SecureWork.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods = 'GET')
    def delete_secureguards_pk_works_pk(self, request, secureguard_pk, work_pk):
        """ Delete a record according to specific secure_guard, work """
       
        delQuerySet = models.SecureWork.objects.filter(secure_pk=secureguard_pk, work_pk=work_pk).all().delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods = 'GET')
    def get_secureguards_pk_works(self, request, secureguard_pk):
        """ Return all work to specific village"""
        querySet = models.SecureWork.objects.filter(secure_pk=secureguard_pk).all()
        serializer = serializers.SecureWorkSerializer(querySet,many=True)
        # result = serializer.data
        secureWork = serializer.data

        # secure = models.SecureGuard.objects.filter(pk=secureguard_pk).last()
        # serializer = serializers.SecureGuardSerializer(secure)
        # secureData = serializer.data
        

        result =[]
        for sw in secureWork:
            swDict= dict()
            swPk = sw['pk']
            # swDict['secure_work_pk'] = sw['pk']
            swDict["secure_pk"] =  sw['secure_pk']
            # swDict['secure_village'] = secureData['secure_village']
            swDict["work_pk"] =  sw['work_pk']
            work = models.Work.objects.filter(pk=sw['work_pk']).last()
            serializer = serializers.WorkSerializer(work)
            workData = serializer.data
            swDict['work_name'] =  workData['work_name']
            swDict['work_start_time'] =  workData['work_start_time']
            swDict['work_end_time'] =  workData['work_end_time']
            swDict['work_hour_split'] = workData['work_hour_split']
            secure = models.SecureGuard.objects.filter(pk=secureguard_pk).last()
            result.append(swDict)

        return notFoundHandling(result)


class QrCodeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.QrCodeSerializer
    queryset = models.Qrcode.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods = 'GET')
    def get_qrcodes_history_additionaldetail(self, request, qrcode_pk):

        isExistQrcode = models.Qrcode.objects.filter(pk=qrcode_pk, is_active=True).exists()
        if(isExistQrcode==False):
            return Response({ "detail": "not have this qrcode "},status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = models.Qrcode.objects.get(pk=qrcode_pk, is_active=True)
            serializer = serializers.QrCodeSerializer(queryset)
            qrCode = serializer.data
            
            result = dict()
            result['enter_secure_name'] = None
            result['inside_secure_name'] = None
            result['scanned_user_name'] = None
            result['exit_secure_name'] = None

            if(qrCode['qr_enter_secure']!=None):
                pk = qrCode['qr_enter_secure']
                isExist = models.SecureGuard.objects.filter(pk = pk, is_active = True).exists()
                if(isExist==True):
                    querySet = models.SecureGuard.objects.get(pk = pk, is_active = True)
                    serializer = serializers.SecureGuardSerializer(querySet)
                    data = serializer.data
                    secureName = data['secure_firstname'] + " "+ data['secure_lastname']
                    result['enter_secure_name'] = secureName

            if(qrCode['qr_inside_secure']!=None):
                pk = qrCode['qr_inside_secure']
                isExist = models.SecureGuard.objects.filter(pk = pk, is_active = True).exists()
                if(isExist==True):
                    querySet = models.SecureGuard.objects.get(pk = pk, is_active = True)
                    serializer = serializers.SecureGuardSerializer(querySet)
                    data = serializer.data
                    secureName = data['secure_firstname'] + " "+ data['secure_lastname']
                    result['inside_secure_name'] = secureName

            if(qrCode['qr_user']!=None):
                pk = qrCode['qr_user']
                isExist = models.GeneralUser.objects.filter(pk = pk, is_active = True).exists()
                if(isExist==True):
                    querySet = models.GeneralUser.objects.get(pk = pk, is_active = True)
                    serializer = serializers.GeneralUserSerializer(querySet)
                    data = serializer.data
                    scannedUserName = data['gen_user_firstname'] + " "+ data['gen_user_lastname']
                    result['scanned_user_name'] = scannedUserName

            if(qrCode['qr_exit_secure']!=None):
                pk = qrCode['qr_exit_secure']
                isExist = models.SecureGuard.objects.filter(pk = pk, is_active = True).exists()
                if(isExist==True):
                    querySet = models.SecureGuard.objects.get(pk = pk, is_active = True)
                    serializer = serializers.SecureGuardSerializer(querySet)
                    data = serializer.data
                    secureName = data['secure_firstname'] + " "+ data['secure_lastname']
                    result['exit_secure_name'] = secureName
                
        return notFoundHandling(result)
            

    @action(detail=True, methods=['post'])
    def create_qrcodes_home_pk_nocopon(self, request):
        """ Create qr code from user incase report the vehicle which not have enter history"""
        
        data = request.data 

        isExistHome = models.Home.objects.filter(pk=data['home_pk'], is_active=True).exists()
        if(isExistHome==False):
            return Response({ "detail": "not have this home number "},status=status.HTTP_404_NOT_FOUND)
        else:
            home = models.Home.objects.filter(pk=data['home_pk'], is_active=True).last()
            serializer = serializers.HomeSerializer(home)
            homeData = serializer.data


            ### using in response data back 
            homePk = homeData['pk']
            homeZone = homeData['home_zone']
            # homeLat = homeData['home_lat']
            # homeLon = homeData['home_lon']
            homeVillage = homeData['home_village']
            homeCompany = homeData['home_company']
            homeNumber = homeData['home_number']

        

            ### create qrcode 
            ### example models.Village.objects.only('pk').get(pk=village_pk)
            village = models.Village.objects.only('pk').get(pk=homeVillage)
            zone = models.Zone.objects.only('pk').get(pk=homeZone)
            company = models.Company.objects.only('pk').get(pk=homeCompany)
            home = models.Home.objects.only('pk').get(pk=homePk)
           

            qrcode = models.Qrcode.objects.create(qr_enter_time=datetime.datetime.now(), qr_car_number=data['qr_car_number'],qr_home_number=homeNumber, qr_car_color = data['qr_car_color'], qr_car_brand=data['qr_car_brand'], qr_company = company, qr_village = village, qr_zone =zone, qr_home =home, qr_exit_without_enter=True)
            qrcode.save
            serializer = serializers.QrCodeSerializer(qrcode)

            # ## create notification 
            # genUserQuerySet = models.GeneralUser.objects.filter(gen_user_home= home, is_active=True).all()
            # for user in genUserQuerySet:
            #     print(user)
            #     notification = models.Notification.objects.create(noti_home=home,noti_general_user=user, noti_qr = qrcode)
            #     notification.save()

            return Response(serializer.data,status.HTTP_201_CREATED)
        

    @action(detail=True, methods = 'GET')
    def get_qrcodes_village_pk_home_number_homedetails(self, request, home_number, village_pk):

        # models.PointObservation.objects.only('pk').get(observation_village=village_pk, observation_zone=zone_pk, observation_work=work_pk, observation_secure=secure_pk, observation_date=date)

        isExistVillage= models.Village.objects.filter(pk=village_pk, is_active=True).exists()
        if(isExistVillage==False):
            return Response({ "detail": "not have this village number "},status=status.HTTP_404_NOT_FOUND)
        else:

            village = models.Village.objects.only('pk').get(pk=village_pk, is_active=True)
            currentQuerySet = models.Home.objects.filter(home_number=home_number,home_village=village, is_active=True).all()
            currentSerializer = serializers.HomeSerializer(currentQuerySet,many=True)
            currentData =  currentSerializer.data
            

            result = []
            
            for home in currentData:
                home_dict = dict()
                home_dict["home_pk"] = home["pk"]
                home_dict['home_zone'] = home['home_zone']
                home_dict['home_lat'] = home['home_lat']
                home_dict['home_lon'] = home['home_lon']

                genUserQuerySet = models.GeneralUser.objects.filter(gen_user_home= home_dict["home_pk"], is_active=True).all()
                genUserSerializer = serializers.GeneralUserSerializer(genUserQuerySet, many=True)
                genUserData = genUserSerializer.data
                
                user_list = []
                for user in genUserData:
                    user_list.append(user['pk'])

                home_dict['genuser_pk_list']  = user_list

                secureGuardQuerySet = models.SecureGuard.objects.filter(secure_zone= home_dict["home_zone"], is_active=True).all()
                secureGuardSerializer = serializers.SecureGuardSerializer(secureGuardQuerySet, many=True)
                secureGuardData = secureGuardSerializer.data

                secure_list = []
                for secure in secureGuardData:
                    secure_list.append(secure['pk'])

                home_dict['secure_pk_list'] = secure_list

                result.append(home_dict)
            

            if(len(result)<1 ):
                return Response({ "detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
            if(len(result)>1 ):
                return Response({ "detail": "Error, multiple home"},status=status.HTTP_404_NOT_FOUND)
        
            return notFoundHandling(result[0])
                


    ## qr_inside_screen_services 
    @action(detail=True, methods = 'GET')
    def get_villages_pk_qrcodes(self, request, village_pk):
        """ Return all information specific to qr_inside_screen services """
        querySet = models.Qrcode.objects.filter(qr_village=village_pk, is_active=True, qr_inside_status=False, qr_complete_status=False, qr_exit_without_enter=False).all()
        serializer = serializers.QrCodeSerializer(querySet,many=True)
        qrData = serializer.data
        ### note: if error in this method please delete below and use common way of return result from serializer.data directly
        result = []
        for qr in qrData:
            qrDict = dict()
            qrDict['pk'] =  qr['pk']
            qrDict['qr_content'] = qr['qr_content']
            qrDict['qr_type'] = qr['qr_type']
            qrDict['qr_car_number'] = qr['qr_car_number']
            qrDict['qr_home_number'] = qr['qr_home_number']
            qrDict['qr_car_color'] = qr['qr_car_color']
            qrDict['qr_car_brand'] = qr['qr_car_brand']
            qrDict['qr_home'] = qr['qr_home']
            qrDict['qr_enter_time'] = qr['qr_enter_time']
            qrDict['qr_home_lat'] = qr['qr_home_lat']
            qrDict['qr_home_lon'] =  qr['qr_home_lon']
            qrDict['is_active'] = qr['is_active']

            zone = models.Zone.objects.filter(pk=qr['qr_zone']).last()
            serializer = serializers.ZoneSerializer(zone)
            zoneData = serializer.data
            qrDict['qr_zone_name'] = zoneData['zone_name']

            result.append(qrDict)
            
        return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def get_villages_pk_zone_pk_qrcodes(self, request, village_pk, zone_pk):
        """ Return all information specific to qr_inside_screen services """
        querySet = models.Qrcode.objects.filter(qr_village=village_pk, qr_zone=zone_pk, is_active=True, qr_inside_status=False, qr_complete_status=False, qr_exit_without_enter=False).all()
        serializer = serializers.QrCodeSerializer(querySet,many=True)
        qrData = serializer.data
        ### note: if error in this method please delete below and use common way of return result from serializer.data directly
        result = []
        for qr in qrData:
            qrDict = dict()
            qrDict['pk'] =  qr['pk']
            qrDict['qr_content'] = qr['qr_content']
            qrDict['qr_type'] = qr['qr_type']
            qrDict['qr_car_number'] = qr['qr_car_number']
            qrDict['qr_home_number'] = qr['qr_home_number']
            qrDict['qr_car_color'] = qr['qr_car_color']
            qrDict['qr_car_brand'] = qr['qr_car_brand']
            qrDict['qr_home'] = qr['qr_home']
            qrDict['qr_enter_time'] = qr['qr_enter_time']
            qrDict['qr_home_lat'] = qr['qr_home_lat']
            qrDict['qr_home_lon'] =  qr['qr_home_lon']
            qrDict['is_active'] = qr['is_active']

            zone = models.Zone.objects.filter(pk=qr['qr_zone']).last()
            serializer = serializers.ZoneSerializer(zone)
            zoneData = serializer.data
            qrDict['qr_zone_name'] = zoneData['zone_name']

            result.append(qrDict)
            
        return notFoundHandling(result)

    ## qr_user_screen_services
    @action(detail=True, methods = 'GET')
    def get_villages_pk_homes_pk_qrcodes(self, request, village_pk, home_pk):
        """ Return all information specific to qr_user_services """
        # querySet = models.Qrcode.objects.filter(qr_village=village_pk, qr_home=home_pk, is_active=True, qr_inside_status=False,qr_home_status=False, qr_complete_status=False, qr_exit_without_enter=False).all()
        # serializer = serializers.QrCodeSerializer(querySet,many=True)
        # result = serializer.data
            
        # return notFoundHandling(result)
        
        querySet = models.Qrcode.objects.filter(qr_village=village_pk, qr_home=home_pk, is_active=True, qr_inside_status=False , qr_home_status=False,qr_complete_status=False, qr_exit_without_enter=False).all()
        serializer = serializers.QrCodeSerializer(querySet,many=True)
        qrData = serializer.data
        ### note: if error in this method please delete below and use common way of return result from serializer.data directly
        result = []
        for qr in qrData:
            qrDict = dict()
            qrDict['pk'] =  qr['pk']
            qrDict['qr_content'] = qr['qr_content']
            qrDict['qr_type'] = qr['qr_type']
            qrDict['qr_car_number'] = qr['qr_car_number']
            qrDict['qr_home_number'] = qr['qr_home_number']
            qrDict['qr_car_color'] = qr['qr_car_color']
            qrDict['qr_car_brand'] = qr['qr_car_brand']
            qrDict['qr_home'] = qr['qr_home']
            qrDict['qr_enter_time'] = qr['qr_enter_time']
            qrDict['qr_home_lat'] = qr['qr_home_lat']
            qrDict['qr_home_lon'] =  qr['qr_home_lon']
            qrDict['is_active'] = qr['is_active']

            zone = models.Zone.objects.filter(pk=qr['qr_zone']).last()
            serializer = serializers.ZoneSerializer(zone)
            zoneData = serializer.data
            qrDict['qr_zone_name'] = zoneData['zone_name']

            result.append(qrDict)
            
        return notFoundHandling(result)

     ## qr_exit_screen_services
    @action(detail=True, methods = 'GET')
    def get_villages_pk_contents_content_qrcodes(self, request, village_pk, content):
        """ Return lasted qr code that match with qr code content """
        querySet = models.Qrcode.objects.filter(qr_village=village_pk, qr_content = content,is_active=True).order_by('qr_enter_time').all()[::-1][:1]
        serializer = serializers.QrCodeSerializer(querySet,many=True)
        result = serializer.data

        error_message="Not found."
        if(len(result)>0):
            return Response(result[0])
        else: 
            return Response({ "detail": error_message},
        status=status.HTTP_404_NOT_FOUND)
    
    ## qr_history_screen_services
    @action(detail=True, methods = 'GET')
    def get_historyservice_list_villages_pk_zones_pk_dates_year_month_day_qrcodes(self, request, village_pk, zone_pk, year, month, day):
        """ Return all qr codeinformation specific for qr history list service """
        querySet = models.Qrcode.objects.filter(qr_village=village_pk, qr_zone = zone_pk, qr_enter_time__date= datetime.date(year,month,day) ,is_active=True).order_by('qr_enter_time').all()[::-1]
        serializer = serializers.QrCodeSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)

     ## qr_history_screen_services
    @action(detail=True, methods = 'GET')
    def get_historyservice_list_villages_pk_zones_pk_qrcodes(self, request, village_pk, zone_pk):
        """ Return all qr codeinformation specific for qr history list service """
        querySet = models.Qrcode.objects.filter(qr_village=village_pk, qr_zone = zone_pk, is_active=True).order_by('qr_enter_time').all()[::-1]
        serializer = serializers.QrCodeSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)

    ## qr_history_screen_services
    @action(detail=True, methods = 'GET')
    def get_historyservice_list_villages_pk_dates_year_month_day_qrcodes(self, request, village_pk, year, month, day):
        """ Return all qr codeinformation specific for qr history list service """
        querySet = models.Qrcode.objects.filter(qr_village=village_pk, qr_enter_time__date= datetime.date(year,month,day) ,is_active=True).order_by('qr_enter_time').all()[::-1]
        serializer = serializers.QrCodeSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)

    ## qr_history_screen_services
    @action(detail=True, methods = 'GET')
    def get_historyservice_list_villages_pk_qrcodes(self, request, village_pk):
        """ Return all qr codeinformation specific for qr history list service """
        querySet = models.Qrcode.objects.filter(qr_village=village_pk, is_active=True).order_by('qr_enter_time').all()[::-1]
        serializer = serializers.QrCodeSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)


class SettingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SettingSerializer
    queryset = models.Setting.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods='GET')
    def get_village_pk_setting(self, request, village_pk):

        isExist = models.Village.objects.filter(pk=village_pk).exists()
        if(isExist==False):
           return Response({ "detail": "Not found village"},status=status.HTTP_404_NOT_FOUND)
        else:
            village=  models.Village.objects.only('pk').get(pk=village_pk)


            isSettingExist = models.Setting.objects.filter(setting_village=village).exists()
            if(isSettingExist==False):
                ### create new setting 
                setting = models.Setting.objects.create(setting_village=village)
                setting.save
                serializer = serializers.SettingSerializer(setting)

                return Response(serializer.data,status.HTTP_201_CREATED)

            else:
                querySet = models.Setting.objects.get(setting_village=village)
                serializer = serializers.SettingSerializer(querySet)
                result = serializer.data

                return notFoundHandling(result)



class PointObservationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PointObservationSerializer
    queryset = models.PointObservation.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods='GET')
    def fetch_pointobservation_update_work(self, request, work_pk):
        workQuerySet = models.Work.objects.filter(pk=work_pk).last()
        serializer = serializers.WorkSerializer(workQuerySet)
        workData = serializer.data
        ### filter by select only sepecific data field
        newWorkData = dict()
        newWorkData['work_start_time'] = workData['work_start_time']
        newWorkData['work_end_time'] = workData['work_end_time']
        newWorkData['work_hour_split'] = workData['work_hour_split']
        
        return notFoundHandling(newWorkData)

    @action(detail=True, methods='GET')
    def fetch_pointobservation_update_zone(self, request, zone_pk):
        zoneQuerySet = models.Zone.objects.filter(pk=zone_pk).last()
        serializer = serializers.ZoneSerializer(zoneQuerySet)
        zoneData = serializer.data
        ### filter by select only sepecific data field
        newZoneData = dict()
        newZoneData['zone_name'] = zoneData['zone_name']
        newZoneData['zone_number'] = zoneData['zone_number']
        return notFoundHandling(newZoneData)


    @action(detail=True, methods='GET')
    def fetch_pointobservation_null_zone_null_work(self, request, village_pk, date):
        """Get data for front of working history services, get Point Observation PK, and Secure data"""
        isExistPO = models.PointObservation.objects.filter(observation_village=village_pk, observation_date=date).exists()
        if(isExistPO==False):
            return Response({ "detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
        else:
            pointObservation = models.PointObservation.objects.filter(observation_village=village_pk, observation_date=date).values_list('pk','observation_work','observation_secure')
            
            print(pointObservation)

            
            result = []

            for po in pointObservation:
                pointObservationDict = dict()

                pointObservationPk = po[0]
                workPk = po[1]
                securePk = po[2]
                # print(work_pk)
                workQuerySet = models.Work.objects.filter(pk=workPk).last()
                serializer = serializers.WorkSerializer(workQuerySet)
                workData = serializer.data
                ### filter by select only sepecific data field
                newWorkData = dict()
                newWorkData['pk'] = workData['pk']
                newWorkData['work_name'] = workData['work_name']
                newWorkData['work_start_time'] = workData['work_start_time']
                newWorkData['work_end_time'] = workData['work_end_time']
                newWorkData['work_hour_split'] = workData['work_hour_split']
                


                secureQuerySet = models.SecureGuard.objects.filter(pk=securePk).last()
                serializer = serializers.SecureGuardSerializer(secureQuerySet)
                secureData = serializer.data
                newSecureData = dict()
                newSecureData['secure_firstname'] = secureData['secure_firstname']
                newSecureData['secure_lastname'] = secureData['secure_lastname']
                newSecureData['secure_type'] = secureData['secure_type']
                zonePk = secureData['secure_zone']
                
                zoneQuerySet = models.Zone.objects.filter(pk=zonePk).last()
                serializer = serializers.ZoneSerializer(zoneQuerySet)
                zoneData = serializer.data
                newZoneData = dict()
                newZoneData['zone_name'] = zoneData['zone_name']
                newZoneData['zone_number'] = zoneData['zone_number']
                
                pointObservationDict['pk'] = pointObservationPk
                pointObservationDict['work'] = newWorkData
                pointObservationDict['secure'] = newSecureData
                pointObservationDict['zone'] = newZoneData

                result.append(pointObservationDict)
            
            return notFoundHandling(result)

    @action(detail=True, methods='GET')
    def fetch_pointobservation_null_zone(self, request, village_pk, work_pk, date):
        """Get data for front of working history services, get Point Observation PK, and Secure data"""
        isExistPO = models.PointObservation.objects.filter(observation_village=village_pk, observation_work=work_pk, observation_date=date).exists()
        if(isExistPO==False):
            return Response({ "detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
        else:
            pointObservation = models.PointObservation.objects.filter(observation_village=village_pk, observation_work=work_pk, observation_date=date).values_list('pk','observation_work','observation_secure')
            
            print(pointObservation)

            
            result = []

            for po in pointObservation:
                pointObservationDict = dict()

                pointObservationPk = po[0]
                workPk = po[1]
                securePk = po[2]
                # print(work_pk)
                workQuerySet = models.Work.objects.filter(pk=workPk).last()
                serializer = serializers.WorkSerializer(workQuerySet)
                workData = serializer.data
                ### filter by select only sepecific data field
                newWorkData = dict()
                newWorkData['pk'] = workData['pk']
                newWorkData['work_name'] = workData['work_name']
                newWorkData['work_start_time'] = workData['work_start_time']
                newWorkData['work_end_time'] = workData['work_end_time']
                newWorkData['work_hour_split'] = workData['work_hour_split']
            

                secureQuerySet = models.SecureGuard.objects.filter(pk=securePk).last()
                serializer = serializers.SecureGuardSerializer(secureQuerySet)
                secureData = serializer.data
                newSecureData = dict()
                newSecureData['secure_firstname'] = secureData['secure_firstname']
                newSecureData['secure_lastname'] = secureData['secure_lastname']
                newSecureData['secure_type'] = secureData['secure_type']
                zonePk = secureData['secure_zone']
                
                zoneQuerySet = models.Zone.objects.filter(pk=zonePk).last()
                serializer = serializers.ZoneSerializer(zoneQuerySet)
                zoneData = serializer.data
                newZoneData = dict()
                newZoneData['zone_name'] = zoneData['zone_name']
                newZoneData['zone_number'] = zoneData['zone_number']
                
                
                pointObservationDict['pk'] = pointObservationPk
                pointObservationDict['work'] = newWorkData
                pointObservationDict['secure'] = newSecureData
                pointObservationDict['zone'] = newZoneData

                result.append(pointObservationDict)
            
            return notFoundHandling(result)


    @action(detail=True, methods='GET')
    def fetch_pointobservation_null_work(self, request, village_pk, zone_pk, date):
        """Get data for front of working history services, get Point Observation PK, and Secure data"""
        isExistPO = models.PointObservation.objects.filter(observation_village=village_pk, observation_zone=zone_pk, observation_date=date).exists()
        if(isExistPO==False):
            return Response({ "detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
        else:
            pointObservation = models.PointObservation.objects.filter(observation_village=village_pk, observation_zone=zone_pk, observation_date=date).values_list('pk','observation_work','observation_secure')
            print(pointObservation)

            result = []

            for po in pointObservation:
                pointObservationDict = dict()

                pointObservationPk = po[0]
                workPk = po[1]
                securePk = po[2]
                # print(work_pk)
                workQuerySet = models.Work.objects.filter(pk=workPk).last()
                serializer = serializers.WorkSerializer(workQuerySet)
                workData = serializer.data
                ### filter by select only sepecific data field
                newWorkData = dict()
                newWorkData['pk'] = workData['pk']
                newWorkData['work_name'] = workData['work_name']
                newWorkData['work_start_time'] = workData['work_start_time']
                newWorkData['work_end_time'] = workData['work_end_time']
                newWorkData['work_hour_split'] = workData['work_hour_split']
                


                secureQuerySet = models.SecureGuard.objects.filter(pk=securePk).last()
                serializer = serializers.SecureGuardSerializer(secureQuerySet)
                secureData = serializer.data
                newSecureData = dict()
                newSecureData['secure_firstname'] = secureData['secure_firstname']
                newSecureData['secure_lastname'] = secureData['secure_lastname']
                newSecureData['secure_type'] = secureData['secure_type']
                zonePk = secureData['secure_zone']
                
                zoneQuerySet = models.Zone.objects.filter(pk=zonePk).last()
                serializer = serializers.ZoneSerializer(zoneQuerySet)
                zoneData = serializer.data
                newZoneData = dict()
                newZoneData['zone_name'] = zoneData['zone_name']
                newZoneData['zone_number'] = zoneData['zone_number']
                
                
                pointObservationDict['pk'] = pointObservationPk
                pointObservationDict['work'] = newWorkData
                pointObservationDict['secure'] = newSecureData
                pointObservationDict['zone'] = newZoneData

                result.append(pointObservationDict)
            
            return notFoundHandling(result)


    @action(detail=True, methods='GET')
    def fetch_pointobservation(self, request, village_pk, zone_pk, work_pk, date):
        """Get data for front of working history services, get Point Observation PK, and Secure data"""
        isExistPO = models.PointObservation.objects.filter(observation_village=village_pk, observation_zone=zone_pk, observation_work=work_pk, observation_date=date).exists()
        if(isExistPO==False):
            return Response({ "detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
        else:
            pointObservation = models.PointObservation.objects.filter(observation_village=village_pk, observation_zone=zone_pk, observation_work=work_pk, observation_date=date).values_list('pk','observation_work','observation_secure')
            
            print(pointObservation)

            
            result = []

            for po in pointObservation:
                pointObservationDict = dict()

                pointObservationPk = po[0]
                workPk = po[1]
                securePk = po[2]
                # print(work_pk)
                workQuerySet = models.Work.objects.filter(pk=workPk).last()
                serializer = serializers.WorkSerializer(workQuerySet)
                workData = serializer.data
                ### filter by select only sepecific data field
                newWorkData = dict()
                newWorkData['pk'] = workData['pk']
                newWorkData['work_name'] = workData['work_name']
                newWorkData['work_start_time'] = workData['work_start_time']
                newWorkData['work_end_time'] = workData['work_end_time']
                newWorkData['work_hour_split'] = workData['work_hour_split']

                secureQuerySet = models.SecureGuard.objects.filter(pk=securePk).last()
                serializer = serializers.SecureGuardSerializer(secureQuerySet)
                secureData = serializer.data
                newSecureData = dict()
                newSecureData['secure_firstname'] = secureData['secure_firstname']
                newSecureData['secure_lastname'] = secureData['secure_lastname']
                newSecureData['secure_type'] = secureData['secure_type']
                zonePk = secureData['secure_zone']
        
                zoneQuerySet = models.Zone.objects.filter(pk=zonePk).last()
                serializer = serializers.ZoneSerializer(zoneQuerySet)
                zoneData = serializer.data
                newZoneData = dict()
                newZoneData['zone_name'] = zoneData['zone_name']
                newZoneData['zone_number'] = zoneData['zone_number']
                
                

                    
                pointObservationDict['pk'] = pointObservationPk
                pointObservationDict['work'] = newWorkData
                pointObservationDict['secure'] = newSecureData
                pointObservationDict['zone'] = newZoneData

                result.append(pointObservationDict)
            
            return notFoundHandling(result)


    @action(detail=True, methods='GET')
    def pointobservation_fetch_record(self, request, village_pk, zone_pk, work_pk, secure_pk, date, timeslot):
        """ Get all Point Observation Record specific to this Point Observation parameter """
        isExistPO = models.PointObservation.objects.filter(observation_village=village_pk, observation_zone=zone_pk, observation_work=work_pk, observation_secure=secure_pk, observation_date=date).exists()
        if(isExistPO==False):
            return Response({ "detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
        else:
            pointObservation = models.PointObservation.objects.only('pk').get(observation_village=village_pk, observation_zone=zone_pk, observation_work=work_pk, observation_secure=secure_pk, observation_date=date)

            querySet = models.PointObservationRecord.objects.all()

            serializer = serializers.PointObservationRecordSerializer(querySet,many=True)
            
            result = serializer.data
            return notFoundHandling(result)


    @action(detail=True, methods='GET')
    def pointobservation_fetch_record_checked_pk(self, request, village_pk, zone_pk, work_pk, secure_pk, date, timeslot):
        """ Get all Point Observation Record specific to this Point Observation parameter """
        isExistPO = models.PointObservation.objects.filter(observation_village=village_pk, observation_zone=zone_pk, observation_work=work_pk, observation_secure=secure_pk, observation_date=date).exists()
        if(isExistPO==False):
            return Response({ "detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
        else:
            pointObservation = models.PointObservation.objects.only('pk').get(observation_village=village_pk, observation_zone=zone_pk, observation_work=work_pk, observation_secure=secure_pk, observation_date=date)

            querySet = models.PointObservationRecord.objects.filter(observation_pk=pointObservation, observation_timeslot=timeslot).values_list('checkpoint_pk', flat=True)
        
            return notFoundHandling(querySet)
    
    
    @action(detail=True, methods=['post'])
    def testObservation(self, request):
        """ Test def"""
        data = request.data
        
        isExistPO = models.PointObservation.objects.filter(observation_village=data['observation_village'], observation_zone=data['observation_zone'], observation_work=data['observation_work'], observation_secure=data['observation_secure'], observation_date=data['observation_date']).exists()
        
        
        if(isExistPO==True):
            ## already have pointObservation
            pointObservation = models.PointObservation.objects.only('pk').get(observation_village=data['observation_village'], observation_zone=data['observation_zone'], observation_work=data['observation_work'], observation_secure=data['observation_secure'], observation_date=data['observation_date'])
            pointPkList = models.Checkpoint.objects.filter(point_zone=data['observation_zone'],is_active=True, point_active=True).values_list('pk', flat=True)
            for pointPk in pointPkList: ## all point 
                checkpoint = models.Checkpoint.objects.only('pk').get(pk=pointPk)
                isExistPOPL = models.PointObservationPointList.objects.filter(observation_pk=pointObservation, checkpoint_pk=checkpoint).exists()
                if(isExistPOPL==False):
                    pointObservationPointList = models.PointObservationPointList.objects.create(observation_pk=pointObservation, checkpoint_pk = checkpoint)
                    pointObservationPointList.save()

            ## check the exist PointObservationRecord
            isExistPOR = models.PointObservationRecord.objects.filter(observation_pk=pointObservation, observation_timeslot=data['observation_timeslot'],checkpoint_pk = data['checkpoint_pk']).exists()
            if(isExistPOR==True):
                ## already have pointObservationRecord
                pointObservationRecord = models.PointObservationRecord.objects.only('pk').get(observation_pk=pointObservation, observation_timeslot=data['observation_timeslot'],checkpoint_pk = data['checkpoint_pk'])
                return Response({ "detail": 'already have this pointObservation and pointObservationRecord'},status=status.HTTP_200_OK)
            else:
                ## create new  pointObservationRecord
                checkpoint = models.Checkpoint.objects.only('pk').get(pk=data['checkpoint_pk'])
                pointObservationRecord = models.PointObservationRecord.objects.create(observation_checkin_time=data['observation_checkin_time'], observation_checkout_time=data['observation_checkout_time'],observation_timeslot=data['observation_timeslot'],checkpoint_pk = checkpoint, observation_pk= pointObservation )
                pointObservationRecord.save()

                serializer = serializers.PointObservationRecordSerializer(pointObservationRecord)

                return Response(serializer.data,status.HTTP_201_CREATED)
        else:
            ## create new  pointObservation
            village = models.Village.objects.only('pk').get(pk=data['observation_village'])
            zone = models.Zone.objects.only('pk').get(pk=data['observation_zone'])
            work = models.Work.objects.only('pk').get(pk=data['observation_work'])
            secure = models.SecureGuard.objects.only('pk').get(pk=data['observation_secure'])
            pointObservation = models.PointObservation.objects.create(observation_village=village, observation_zone=zone, observation_work=work, observation_secure=secure, observation_date=data['observation_date'])
            pointObservation.save()

            ## create new PointObservationRecord
            pointPkList = models.Checkpoint.objects.filter(point_zone=data['observation_zone'],is_active=True,point_active=True).values_list('pk', flat=True)
            for pointPk in pointPkList: ## all point 
                checkpoint = models.Checkpoint.objects.only('pk').get(pk=pointPk)
                pointObservationPointList = models.PointObservationPointList.objects.create(observation_pk=pointObservation, checkpoint_pk = checkpoint)
                pointObservationPointList.save()


            isExistPOR = models.PointObservationRecord.objects.filter(observation_pk=pointObservation, observation_timeslot=data['observation_timeslot'],checkpoint_pk = data['checkpoint_pk']).exists()
            if(isExistPOR==True):
                ## already have pointObservationRecord
                pointObservationRecord = models.PointObservationRecord.objects.only('pk').get(observation_pk=pointObservation, observation_timeslot=data['observation_timeslot'],checkpoint_pk = data['checkpoint_pk'])
                return Response({ "detail": 'already have this pointObservationRecord'},status=status.HTTP_200_OK)
            else:
                ## create new  pointObservationRecord
                checkpoint = models.Checkpoint.objects.only('pk').get(pk=data['checkpoint_pk'])
                pointObservationRecord = models.PointObservationRecord.objects.create(observation_checkin_time=data['observation_checkin_time'], observation_checkout_time=data['observation_checkout_time'],observation_timeslot=data['observation_timeslot'],checkpoint_pk = checkpoint, observation_pk= pointObservation )
                pointObservationRecord.save()

                serializer = serializers.PointObservationRecordSerializer(pointObservationRecord)

                return Response(serializer.data,status.HTTP_201_CREATED)


       


class PointObservationPointListViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PointObservationPointListSerializer
    queryset = models.PointObservationPointList.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods='GET')
    def fetch_pointobservationrecord_pointlist(self, request, pointobservation_pk, timeslot):
        """Get data for detail of working history services"""

      
        isExistPO = models.PointObservation.objects.filter(pk=pointobservation_pk).exists()

        if(isExistPO==False):
            return Response({ "detail": "Not found point observation."},status=status.HTTP_404_NOT_FOUND)
        else:

            pointPkList = models.PointObservationPointList.objects.filter(observation_pk=pointobservation_pk).values_list('checkpoint_pk', flat=True)
            
            result = []
            ### each point pk
            for pointPk in pointPkList:
                    
                pointDict = dict()
                pointDict['pk'] = pointPk
                
                
                checkpointQuerySet = models.Checkpoint.objects.filter(pk=pointPk).all()
                serializer = serializers.CheckpointSerializer(checkpointQuerySet, many=True)
                checkpoint = serializer.data

                pointDict['point_name'] = checkpoint[0]['point_name']
                pointDict['point_lat'] = checkpoint[0]['point_lat']
                pointDict['point_lon']= checkpoint[0]['point_lon']
                
                isExistPOR = models.PointObservationRecord.objects.filter(observation_pk=pointobservation_pk, observation_timeslot= timeslot, checkpoint_pk = pointPk).exists()

                if(isExistPOR==False):
                    pointDict['checked_status'] = False
                    pointDict['checkin_time']= None
                    pointDict['checkout_time'] = None
                    result.append(pointDict)
                else: 
                    porQuerySet = models.PointObservationRecord.objects.filter(observation_pk=pointobservation_pk, observation_timeslot= timeslot).all()
                    serializer = serializers.PointObservationRecordSerializer(porQuerySet,many=True)
                    porData = serializer.data
                    
                    pointDict['check_status'] = True
                    pointDict['checkin_time'] = porData[0]['observation_checkin_time']
                    pointDict['checkout_time'] = porData[0]['observation_checkout_time']

                    result.append(pointDict)

            return notFoundHandling(result)
            
            # pointNum = models.PointObservationPointList.objects.filter(observation_pk=pointobservation_pk ).count()
            # checkedPointNum = models.PointObservationRecord.objects.filter(observation_pk=pointobservation_pk, observation_timeslot=timeslot).count()
            
            # result = {'percent':int((checkedPointNum/pointNum)*100)}

            # return notFoundHandling(result)


    

class PointObservationRecordViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PointObservationRecordSerializer
    queryset = models.PointObservationRecord.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)



    @action(detail=True, methods='GET')
    def fetch_pointobservationrecord_percent(self, request, pointobservation_pk, timeslot):
        """Get data for front of working history services, get Point Observation PK, and Secure data"""
        # print(pointobservation_pk)
        # print(timeslot)
        # pointObservation = models.PointObservation.objects.only('pk').get(pk=pointobservation_pk)
        isExistPO = models.PointObservation.objects.filter(pk=pointobservation_pk).exists()

        if(isExistPO==False):
            return Response({ "detail": "Not found point observation."},status=status.HTTP_404_NOT_FOUND)
        else:
            pointNum = models.PointObservationPointList.objects.filter(observation_pk=pointobservation_pk ).count()
            checkedPointNum = models.PointObservationRecord.objects.filter(observation_pk=pointobservation_pk, observation_timeslot=timeslot).count()
            
            result = {'percent':int((checkedPointNum/pointNum)*100)}

            return notFoundHandling(result)

    @action(detail=True, methods='GET')
    def fetch_pointobservationrecord_timeslots_percent(self, request, pointobservation_pk):
        """Get data for front of working history services, get Point Observation PK, and Secure data"""
        # print(pointobservation_pk)
        # print(timeslot)
        # pointObservation = models.PointObservation.objects.only('pk').get(pk=pointobservation_pk)
        isExistPO = models.PointObservation.objects.filter(pk=pointobservation_pk).exists()

        if(isExistPO==False):
            return Response({ "detail": "Not found point observation."},status=status.HTTP_404_NOT_FOUND)
        else:
            pointNum = models.PointObservationPointList.objects.filter(observation_pk=pointobservation_pk ).count()

            pointObservationRecord = models.PointObservationRecord.objects.filter(observation_pk=pointobservation_pk).values('observation_timeslot').order_by().annotate(Count('checkpoint_pk'))

            result = []
            for item in pointObservationRecord:
                temp = dict()
                temp['timeslot'] = item['observation_timeslot']
                temp['percent'] =  int((item['checkpoint_pk__count']/pointNum)*100)
                result.append(temp)

            return notFoundHandling(result)


class MaintenanceFeePeriodViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MaintenanceFeePeriodSerializer
    queryset = models.MaintenanceFeePeriod.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods = 'GET')
    def get_maintenance_fee_period_total_amount_number_paid_home(self, request, pk):
        """ Return total amount and number of paid home according to specific MaintenanceFeePeriod"""
        
        isExistMtp = models.MaintenanceFeePeriod.objects.filter(pk=pk, is_active=True).exists()
        if(isExistMtp==False):
            return Response({ "detail": "Not have this maintenance fee period"},status=status.HTTP_404_NOT_FOUND)
        else:

            maintenancefeeperiod = models.MaintenanceFeePeriod.objects.only('pk').get(pk=pk)
            paidHomeNum = models.MaintenanceFeeRecord.objects.filter(fee_period=maintenancefeeperiod,fee_paid_status=True,is_active=True).count()
            totalAmount = models.MaintenanceFeeRecord.objects.filter(fee_period=maintenancefeeperiod,fee_paid_status=True,is_active=True).aggregate(Sum('fee_amount'))['fee_amount__sum']
            
            print(paidHomeNum)
            print(totalAmount)
            result = {"total_amount": totalAmount, "paid_home_number":paidHomeNum}
    
            return notFoundHandling(result)

  
    @action(detail=True, methods = 'GET')
    def get_villages_pk_maintenance_fee_period(self, request, village_pk):
        """ Return all maintenance fee period according to specific village """
        querySet = models.MaintenanceFeePeriod.objects.filter(fee_village=village_pk,is_active=True).all()
        
        result = []
        for maintenancefeeperiod in querySet:
            homeNum = models.MaintenanceFeeRecord.objects.filter(fee_period=maintenancefeeperiod,is_active=True).count()
            paidHomeNum = models.MaintenanceFeeRecord.objects.filter(fee_period=maintenancefeeperiod,fee_paid_status=True,is_active=True).count()
            totalAmount = models.MaintenanceFeeRecord.objects.filter(fee_period=maintenancefeeperiod,fee_paid_status=True,is_active=True).aggregate(Sum('fee_amount'))['fee_amount__sum']
            serializer = serializers.MaintenanceFeePeriodSerializer(maintenancefeeperiod)
            mfp = serializer.data
            if(totalAmount==None):
                totalAmount=0
            if(paidHomeNum==None):
                paidHomeNum=0
            if(homeNum==None):
                homeNum=0
            mfp['total_amount'] = totalAmount
            mfp['home_number'] = homeNum
            mfp['paid_home_number'] = paidHomeNum
            result.append(mfp)

        return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def get_villages_pk_maintenance_fee_period_pk(self, request, village_pk, mfpPk):
        """ Return all maintenance fee period according to specific village """
        maintenancefeeperiod = models.MaintenanceFeePeriod.objects.filter(fee_village=village_pk, pk=mfpPk,is_active=True).last()
        homeNum = models.MaintenanceFeeRecord.objects.filter(fee_period=maintenancefeeperiod,is_active=True).count()
        paidHomeNum = models.MaintenanceFeeRecord.objects.filter(fee_period=maintenancefeeperiod,fee_paid_status=True,is_active=True).count()
        totalAmount = models.MaintenanceFeeRecord.objects.filter(fee_period=maintenancefeeperiod,fee_paid_status=True,is_active=True).aggregate(Sum('fee_amount'))['fee_amount__sum']
        serializer = serializers.MaintenanceFeePeriodSerializer(maintenancefeeperiod)
        if(totalAmount==None):
            totalAmount=0
        if(paidHomeNum==None):
            paidHomeNum=0
        if(homeNum==None):
            homeNum=0
        result = serializer.data
        result['total_amount'] = totalAmount
        result['home_number'] = homeNum
        result['paid_home_number'] = paidHomeNum
        
        return notFoundHandling(result)
        # serializer = serializers.MaintenanceFeePeriodSerializer(querySet,many=True)
        # result = serializer.data

            
       

    
    @action(detail=True, methods=['post'])
    def create_maintenance_fee_period(self, request):
        """ Create maintenance fee period record along with all of maintenance fee record for each home in that village"""

        data = request.data 

        isExistVillage = models.Village.objects.filter(pk = data['fee_village']).exists()

        if(isExistVillage==False):
            return Response({ "detail": "not have this village to for creating maintenance_fee_period "},status=status.HTTP_404_NOT_FOUND)
        else:
            village = models.Village.objects.get(pk=data['fee_village'])
            maintenanceFeePeriod = models.MaintenanceFeePeriod.objects.create(fee_village = village, fee_period_name= data['fee_period_name'], fee_start= data['fee_start'], fee_end=data['fee_end'], fee_deadline = data['fee_deadline'], is_active = True)
            maintenanceFeePeriod.save()
            serializer = serializers.MaintenanceFeePeriodSerializer(maintenanceFeePeriod)

            ## create maintenance fee record for all home in this village 
            homes = models.Home.objects.filter(home_village=village)
            for home in homes:
                print(home)
                print(type(home))
                
                maintenanceFeeRecord = models.MaintenanceFeeRecord.objects.create(fee_period=maintenanceFeePeriod, fee_home=home,fee_paid_date=None, fee_house_space=None, fee_amount=None, fee_paid_status=False, is_active=True)
                maintenanceFeeRecord.save()

            

            return Response(serializer.data,status.HTTP_201_CREATED)

     

class MaintenanceFeeRecordViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MaintenanceFeeRecordSerializer
    queryset = models.MaintenanceFeeRecord.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods = 'GET')
    def mtr_check_isexist_and_isduplicate_home(self, request, home_number, mfp_pk):
        """ Check is home exist and is this home already exist in this mfp"""
        isExist = models.Home.objects.filter(home_number=home_number, is_active=True).exists()
        if(isExist==False):
            return Response({ "detail": "Not have this home number"},status=status.HTTP_404_NOT_FOUND)
        else:
            querySet = models.Home.objects.filter(home_number=home_number, is_active=True).last()
            serializer = serializers.HomeSerializer(querySet)
            result = serializer.data
            # print(result) 
           

            isExistMtp = models.MaintenanceFeePeriod.objects.filter(pk=mfp_pk, is_active=True).exists()
            if(isExistMtp==False):
                return Response({ "detail": "Not have this maintenance fee period"},status=status.HTTP_404_NOT_FOUND)
            else:
                maintenancefeeperiod = models.MaintenanceFeePeriod.objects.only('pk').get(pk=mfp_pk)
                home = models.Home.objects.only('pk').get(home_number=home_number, is_active=True)
                isExist = models.MaintenanceFeeRecord.objects.filter(fee_period=mfp_pk, fee_home = home, is_active=True).exists()

                if(isExist==False):
                    return Response({"pk":result['pk'],"home_number":result['home_number'],"duplicate_check":False})
                else:
                    return Response({"pk":result['pk'],"home_number":result['home_number'],"duplicate_check":True})


    ## qr_history_screen_services
    @action(detail=True, methods = 'GET')
    def get_maintenance_fee_period_pk_maintenance_fee_record(self, request, pk):
        """ Return all maintenance fee record according to specific village and maintenance period"""
        querySet = models.MaintenanceFeeRecord.objects.filter(fee_period = pk, is_active=True).all()
        serializer = serializers.MaintenanceFeeRecordSerializer(querySet,many=True)

        mfrResult = serializer.data
        result = []

        for mfr in mfrResult:
            mfrDict = dict()
            mfrDict['pk'] = mfr['pk']
            mfrDict['fee_period'] = mfr['fee_period']
            mfrDict['fee_home'] = mfr['fee_home']
            mfrDict['fee_paid_date'] = mfr['fee_paid_date']
            mfrDict['fee_house_space'] = mfr['fee_house_space']
            mfrDict['fee_amount'] = mfr['fee_amount']
            mfrDict['fee_paid_status'] = mfr['fee_paid_status']
            mfrDict['is_active'] = mfr['is_active']
            homePk = mfr['fee_home']

            homeQuerySet = models.Home.objects.filter(pk = homePk, is_active=True).last()
            serializer = serializers.HomeSerializer(homeQuerySet)
            homeResult = serializer.data
            mfrDict['home_number'] = homeResult['home_number']
            result.append(mfrDict)
        

        return notFoundHandling(result)


class VoteTopicViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VoteTopicSerializer
    queryset = models.VoteTopic.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    #  @action(detail=True, methods=['post'])
    # def create_enter_qrcode_and_notificaton(self, request):
    #     """ Create qr code on enter screen along with generate notification for each user"""
        
    #     data = request.data 

    @action(detail=True, methods = ['patch'])
    def patch_votetopics_result(self, request, pk):
        votetopic = self.get_object()
        data = request.data
        updateData = {'vote_confirm_status':True}
        voteSerializer = serializers.VoteTopicSerializer(votetopic, updateData, partial=True)
        voteSerializer.is_valid(raise_exception=True)
        voteSerializer.save()
        
        
        
        
        votechoice = models.VoteChoice.objects.get(pk = data['selected_confirm_choice_pk'],is_active=True)
        # print(votechoice)
        updateData = {'vote_is_result':True}
        choiceSerializer = serializers.VoteChoiceSerializer(votechoice, updateData,partial=True)
        choiceSerializer.is_valid(raise_exception=True)
        choiceSerializer.save()

        # print(voteSerializer.data)
        result = voteSerializer.data
        result['votechoice_pk'] = data['selected_confirm_choice_pk']
        result['vote_is_result'] = True


        return Response(result)
        
    # @detail_route(methods=['POST','GET'])
    # def assign(self, request, pk):
    #     rocnation = self.get_object()
    #     data = {'roc_views': rocnation.roc_views + 1}
    #     serializer = RocNationSerializer(rocnation, data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
        

    @action(detail=True, methods = 'GET')
    def get_votetopics_pk_result_admin(self, request, votetopic_pk):
        """ Return result of voting information according to specific village """

        isVoteTopicExist = models.VoteTopic.objects.filter(pk=votetopic_pk,is_active=True).exists()
        if(isVoteTopicExist==False):
            return Response({ "detail": "Not have this vote topics"},status=status.HTTP_404_NOT_FOUND)
        else:
            result = []
            ### find vote topic
            voteTopic = models.VoteTopic.objects.filter(pk=votetopic_pk,is_active=True).last()
            voteTopicTitle = models.VoteTopic.objects.filter(pk=votetopic_pk,is_active=True).values('vote_thai_topic').last()
            # print(voteTopicTitle)
            result.append({"voteTopicTitle":voteTopicTitle['vote_thai_topic']})
            
            ### -----------------------------

            ### find vote record in percent
            
            voteChoices = models.VoteChoice.objects.filter(vote_topic_pk= voteTopic).values('pk','vote_thai_choice','vote_is_result')
            ### dict for keep pk string map to name
            voteChoiceNameDict = dict()
            ### dict for keep pk string map to count number
            voteCountDict = dict()
            for choice in voteChoices:
                voteChoiceNameDict[str(choice['pk'])] = choice['vote_thai_choice']
                voteCountDict[str(choice['pk'])] = 0

            voteRecordsAll = models.VoteRecord.objects.filter(vote_topic_pk=voteTopic).values('vote_selected_choice')

            ### count number of vote record for each choice
            for vote in voteRecordsAll:
                voteCountDict[str(vote['vote_selected_choice'])] = voteCountDict[str(vote['vote_selected_choice'])]+1

            percent_result = []
            voteRecordsCountAll = models.VoteRecord.objects.filter(vote_topic_pk=voteTopic).count()
            for choice in voteChoices:
                resultDict = dict()
                
                resultDict['voteChoicePk'] = choice['pk']
                resultDict['voteChoiceTitle'] = choice['vote_thai_choice']
                resultDict['voteChoiceIsResult'] = choice['vote_is_result']
                resultDict['count'] = voteCountDict[str(choice['pk'])]
                if(voteRecordsCountAll==0):
                    resultDict['percent'] = 0
                else:
                    resultDict['percent'] = (resultDict['count']/voteRecordsCountAll)*100

                percent_result.append(resultDict)

            result.append(percent_result)

            
            ### -----------------------------
        
            ##-------------------------------
            ##---old method------------------

            # ### find vote record in percent
            # voteRecords = models.VoteRecord.objects.filter(vote_topic_pk=voteTopic).values('vote_selected_choice').order_by('vote_selected_choice').annotate(count=Count('vote_selected_choice'))
            # voteRecordsCountAll = models.VoteRecord.objects.filter(vote_topic_pk=voteTopic).count()

            
            # percent_result= []
            # for voteRecord in voteRecords:
            #     resultDict = dict()
                
            #     voteChoicePk = voteRecord['vote_selected_choice']

                
            #     voteChoice = models.VoteChoice.objects.filter(pk = voteChoicePk).values('vote_thai_choice').last()
            #     resultDict['voteChocePk'] = voteRecord['vote_selected_choice']
            #     resultDict['voteChoiceTitle'] = voteChoice['vote_thai_choice']
            #     resultDict['count'] = voteRecord['count']
            #     resultDict['percent'] = (resultDict['count']/voteRecordsCountAll)*100
                

            #     percent_result.append(resultDict)
            
            # result.append(percent_result)


            ##-------------------------------

            ## find vote record for individual home
            voteRecords = models.VoteRecord.objects.filter(vote_topic_pk=voteTopic).values('vote_home','vote_selected_choice','vote_hiden').order_by('vote_selected_choice')

            individual_result = []
            for voteRecord in voteRecords:
                resultDict = dict()
                
                
                homePk = voteRecord['vote_home']
                voteChoicePk = voteRecord['vote_selected_choice']
                
                home = models.Home.objects.filter(pk=homePk).values('home_number').last()
                voteChoice = models.VoteChoice.objects.filter(pk = voteChoicePk).values('vote_thai_choice').last()
                resultDict['homePk'] = voteRecord['vote_home']
                resultDict['homeNumber'] = home['home_number']
               
                resultDict['voteChoiceTitle'] = voteChoice['vote_thai_choice']
                resultDict['voteChoicePk'] = voteRecord['vote_selected_choice']
                

                individual_result.append(resultDict)

            result.append(individual_result)

            return notFoundHandling(result)


    @action(detail=True, methods = 'GET')
    def get_votetopics_pk_result_user_home_pk(self, request, votetopic_pk, home_pk):
        """ Return result of voting information according to specific village """

        isVoteTopicExist = models.VoteTopic.objects.filter(pk=votetopic_pk,is_active=True).exists()
        if(isVoteTopicExist==False):
            return Response({ "detail": "Not have this vote topics"},status=status.HTTP_404_NOT_FOUND)
        else:
            result = []
            ### find vote topic
            voteTopic = models.VoteTopic.objects.filter(pk=votetopic_pk,is_active=True).last()
            voteTopicTitle = models.VoteTopic.objects.filter(pk=votetopic_pk,is_active=True).values('vote_thai_topic').last()
            print(voteTopicTitle)
            result.append({"voteTopicTitle":voteTopicTitle['vote_thai_topic']})

            ### find vote record in percent
            voteRecords = models.VoteRecord.objects.filter(vote_topic_pk=voteTopic).values('vote_selected_choice').order_by('vote_selected_choice').annotate(count=Count('vote_selected_choice'))
            voteRecordsCountAll = models.VoteRecord.objects.filter(vote_topic_pk=voteTopic).count()

            percent_result= []
            for voteRecord in voteRecords:
                resultDict = dict()
                
                voteChoicePk = voteRecord['vote_selected_choice']

                
                voteChoice = models.VoteChoice.objects.filter(pk = voteChoicePk).values('vote_thai_choice').last()
                resultDict['voteChocePk'] = voteRecord['vote_selected_choice']
                resultDict['voteChoiceTitle'] = voteChoice['vote_thai_choice']
                resultDict['count'] = voteRecord['count']
                resultDict['percent'] = (resultDict['count']/voteRecordsCountAll)*100
                

                percent_result.append(resultDict)
            
            

            ## find vote record for individual home
            voteRecords = models.VoteRecord.objects.filter(vote_topic_pk=voteTopic).values('vote_home','vote_selected_choice','vote_hiden').order_by('vote_selected_choice')

            individual_result = []
            for voteRecord in voteRecords:
                resultDict = dict()
                
                
                homePk = voteRecord['vote_home']
                voteChoicePk = voteRecord['vote_selected_choice']
                
                home = models.Home.objects.filter(pk=homePk).values('home_number').last()
                voteChoice = models.VoteChoice.objects.filter(pk = voteChoicePk).values('vote_thai_choice').last()
                resultDict['homePk'] = voteRecord['vote_home']
                resultDict['homeNumber'] = home['home_number']
                if(resultDict['homePk']==home_pk):
                    result[0]['currentHomePk'] = voteRecord['vote_home']
                    result[0]['currentChoiceTitle'] = voteChoice['vote_thai_choice']
                    resultDict['voteChoiceTitle'] = voteChoice['vote_thai_choice']
                    resultDict['voteChoicePk'] = voteRecord['vote_selected_choice']
                else:
                    if(voteRecord['vote_hiden']==True):
                        resultDict['voteChoiceTitle'] = "ไม่เปิดเผย"
                        resultDict['voteChoicePk'] = "ไม่เปิดเผย"
                    else:
                        resultDict['voteChoiceTitle'] = voteChoice['vote_thai_choice']
                        resultDict['voteChoicePk'] = voteRecord['vote_selected_choice']
                

                individual_result.append(resultDict)

            result.append(percent_result)
            result.append(individual_result)

            return notFoundHandling(result)
                
               

    
    @action(detail=True, methods = 'GET')
    def get_villages_pk_votetopics(self, request, village_pk):
        """ Return all votetopics according to specific village """
        querySet = models.VoteTopic.objects.filter(vote_village=village_pk,is_active=True).all()
        serializer = serializers.VoteTopicSerializer(querySet, many=True)
        result = serializer.data 

        return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def get_villages_pk_user_pk_votetopics(self, request, village_pk, home_pk):
        """ Return all votetopics which the user not vote yet according to specific village """
        
        querySet = models.VoteTopic.objects.filter(vote_village=village_pk, vote_end_date__gte=datetime.date.today(), vote_confirm_status=False,is_active=True).all()
        serializer = serializers.VoteTopicSerializer(querySet, many=True)
        result = serializer.data 

        isHomeExist = models.Home.objects.filter(pk=home_pk).exists()
        if(isHomeExist==False):
            return Response({ "detail": "Not have this home"},status=status.HTTP_404_NOT_FOUND)
        else:
            # home = models.Home.objects.only('pk').get(pk=home_pk)

            home = models.Home.objects.get(pk=home_pk,is_active=True)
            serializer = serializers.HomeSerializer(home)
            print()
            voteQuota = serializer.data['home_vote_qouta']

            result = []
            for voteTopic in querySet:
                ### filter vote whether already vote or not 
                voteCount = models.VoteRecord.objects.filter(vote_topic_pk=voteTopic, vote_home = home).count()
                if(voteCount < voteQuota):
                    serializer = serializers.VoteTopicSerializer(voteTopic)
                    voteTopicData = serializer.data
                    voteTopicData['num_vote_left']= voteQuota - voteCount
                    result.append(voteTopicData)

                    

            return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def checkvoteable_village_pk_home_pk(self, request, village_pk, home_pk):
        """ Return all votetopics which the user not vote yet according to specific village """
        ### check village exists
        isVilExist = models.Village.objects.filter(pk=village_pk,is_active=True).exists()
        if(isVilExist==False):
            return Response({ "detail": "Not have this village"},status=status.HTTP_404_NOT_FOUND)
        else:
            villageObject = models.Village.objects.only('pk').get(pk=village_pk,is_active=True)
            feePeriodObject = models.MaintenanceFeePeriod.objects.only('pk').filter(fee_village= villageObject,fee_deadline__lt=datetime.date.today(),is_active=True)

            isHomeExist = models.Home.objects.filter(pk=home_pk,is_active=True).exists()
            if(isHomeExist==False):
                return Response({ "detail": "Not have this home"},status=status.HTTP_404_NOT_FOUND)
            else:
                ## check home exists 
                homeObject = models.Home.objects.only('pk').get(pk=home_pk,is_active=True)
                

                isVoteAble = True

                ### loop for each period that is this village 
                for feePeriod in feePeriodObject:
                    feeRecordObject  = models.MaintenanceFeeRecord.objects.filter(fee_period=feePeriod,fee_home=homeObject, is_active=True).all()
                    serializer = serializers.MaintenanceFeeRecordSerializer(feeRecordObject,many=True)
                    feeRecordData = serializer.data
                    ### loop for each record that is this home 
                    for feeRec in feeRecordData:
                        print(feeRec)
                        if(feeRec['fee_paid_status']==False):
                            isVoteAble= False
                            break
                         
                return notFoundHandling([{'voteAble':isVoteAble}])



            # home = models.Home.objects.only('pk').get(pk=home_pk)

            
            # result = []
            # for voteTopic in querySet:
            #     ### filter vote whether already vote or not 
            #     isVoted = models.VoteRecord.objects.filter(vote_topic_pk=voteTopic, vote_home = home).exists()
            #     if(isVoted==False):
            #         serializer = serializers.VoteTopicSerializer(voteTopic)
            #         result.append(serializer.data)


            # return notFoundHandling(result)

   
        

class VoteChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VoteChoiceSerializer
    queryset = models.VoteChoice.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods = 'GET')
    def get_votetopics_pk_votechoices(self, request, votetopic_pk):
        """ Return all votechoices fee period according to specific votetopic """

        isExist = models.VoteTopic.objects.filter(pk= votetopic_pk, is_active=True).exists()
        if(isExist==False):
            return Response({ "detail": "Not have this maintenance fee period"},status=status.HTTP_404_NOT_FOUND)
        else:
            voteTopic = models.VoteTopic.objects.only('pk').get(pk=votetopic_pk)
            querySet = models.VoteChoice.objects.filter( vote_topic_pk=voteTopic, is_active=True).all()
            serializer = serializers.VoteChoiceSerializer(querySet, many=True)
            result = serializer.data 

            return notFoundHandling(result)

class VoteRecordViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VoteRecordSerializer
    queryset = models.VoteRecord.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class ProblemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProblemSerializer
    queryset = models.Problem.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods = 'GET')
    def get_homes_pk_problems(self, request, home_pk):
        """ Return all votetopics according to specific village """

        isExist = models.Home.objects.filter(pk= home_pk, is_active=True).exists()
        if(isExist==False):
            return Response({ "detail": "Not have this home in system"},status=status.HTTP_404_NOT_FOUND)
        else:
            home = models.Home.objects.only('pk').get(pk=home_pk)
            querySet = models.Problem.objects.filter( problem_home=home, is_active=True).all()
            serializer = serializers.ProblemSerializer(querySet, many=True)
            result = serializer.data 

            return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def get_problems_with_home_number(self, request, village_pk ):
        """ Return all votetopics according to specific village """

        querySet = models.Problem.objects.filter(problem_village = village_pk,is_active=True).all()
        serializer = serializers.ProblemSerializer(querySet, many=True)
        # result = serializer.data 
        problemData = serializer.data 


        result = []
        # print(problemData)
        for problem in problemData:
            newDict = dict()
            print(problem)
            homePk = problem['problem_home']
            home = models.Home.objects.filter(pk = homePk).last()
            serializer = serializers.HomeSerializer(home,)
            homeData = serializer.data
            newDict['pk'] = problem['pk']
            newDict['problem_village'] = problem['problem_village']
            newDict['problem_home'] = problem['problem_home']
            newDict['problem_home_number'] = homeData['home_number']
            newDict['problem_date'] = problem['problem_date']
            newDict['problem_type'] = problem['problem_type']
            newDict['problem_detail'] = problem['problem_detail']
            newDict['problem_feedback'] = problem['problem_feedback']
            newDict['is_active'] = problem['is_active']
            newDict['is_active_admin'] = problem['is_active_admin']
            result.append(newDict)

        return notFoundHandling(result)

class WorkingRecordViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WorkingRecordSerializer
    queryset = models.WorkingRecord.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods = 'GET')
    def get_secure_pk_workingrecord_lasted(self, request, secureguard_pk):
        """ Return all votetopics according to specific village """
        querySet = models.WorkingRecord.objects.filter(working_secure=secureguard_pk).last()
        serializer = serializers.WorkingRecordSerializer(querySet)
        result = serializer.data 

        return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def fetch_workingrecord(self, request, village_pk, zone_pk, work_pk, date_str):
        """ Return all votetopics according to specific village """
        print(date_str)
        newdate = date_str.split("-")
        print(newdate[0])
        isExistWR = models.WorkingRecord.objects.filter(working_village=village_pk, working_zone=zone_pk, working_work=work_pk,working_date__date=datetime.date(int(newdate[0]),int(newdate[1]),int(newdate[2]))).exists()
        if(isExistWR==False):
            return Response({ "detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
        else:
            workingRecord = models.WorkingRecord.objects.filter(working_village=village_pk, working_zone=zone_pk, working_work=work_pk,working_date__date=datetime.date(int(newdate[0]),int(newdate[1]),int(newdate[2]))).values('working_secure','working_work').distinct()
            
            result = []

            for wr in workingRecord:
                # print(wr)
                wrDict = dict()

                workPk = wr['working_work']
                securePk = wr['working_secure']

                workQuerySet = models.Work.objects.filter(pk=workPk).last()
                serializer = serializers.WorkSerializer(workQuerySet)
                workData = serializer.data

                newWorkData = dict()
                newWorkData['pk'] = workData['pk']
                newWorkData['work_name'] = workData['work_name']

                secureQuerySet = models.SecureGuard.objects.filter(pk=securePk).last()
                serializer = serializers.SecureGuardSerializer(secureQuerySet)
                secureData = serializer.data
                newSecureData = dict()
                newSecureData['pk'] = secureData['pk']
                newSecureData['secure_firstname'] = secureData['secure_firstname']
                newSecureData['secure_lastname'] = secureData['secure_lastname']
                newSecureData['secure_type'] = secureData['secure_type']
                zonePk = secureData['secure_zone']

                zoneQuerySet = models.Zone.objects.filter(pk=zonePk).last()
                serializer = serializers.ZoneSerializer(zoneQuerySet)
                zoneData = serializer.data
                newZoneData = dict()
                newZoneData['pk'] = zoneData['pk']
                newZoneData['zone_name'] = zoneData['zone_name']
                newZoneData['zone_number'] = zoneData['zone_number']

                wrDict['work'] = newWorkData
                wrDict['secure'] = newSecureData
                wrDict['zone'] = newZoneData

                result.append(wrDict)
            

            return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def fetch_workingrecord_null_work(self, request, village_pk, zone_pk, date_str):
        """ Return all votetopics according to specific village """
        print(date_str)
        newdate = date_str.split("-")
        print(newdate[0])
        isExistWR = models.WorkingRecord.objects.filter(working_village=village_pk, working_zone=zone_pk, working_date__date=datetime.date(int(newdate[0]),int(newdate[1]),int(newdate[2]))).exists()
        if(isExistWR==False):
            return Response({ "detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
        else:
            workingRecord = models.WorkingRecord.objects.filter(working_village=village_pk, working_zone=zone_pk, working_date__date=datetime.date(int(newdate[0]),int(newdate[1]),int(newdate[2]))).values('working_secure','working_work').distinct()
            
            result = []

            for wr in workingRecord:
                # print(wr)
                wrDict = dict()

                workPk = wr['working_work']
                securePk = wr['working_secure']

                workQuerySet = models.Work.objects.filter(pk=workPk).last()
                serializer = serializers.WorkSerializer(workQuerySet)
                workData = serializer.data

                newWorkData = dict()
                newWorkData['pk'] = workData['pk']
                newWorkData['work_name'] = workData['work_name']

                secureQuerySet = models.SecureGuard.objects.filter(pk=securePk).last()
                serializer = serializers.SecureGuardSerializer(secureQuerySet)
                secureData = serializer.data
                newSecureData = dict()
                newSecureData['pk'] = secureData['pk']
                newSecureData['secure_firstname'] = secureData['secure_firstname']
                newSecureData['secure_lastname'] = secureData['secure_lastname']
                newSecureData['secure_type'] = secureData['secure_type']
                zonePk = secureData['secure_zone']

                zoneQuerySet = models.Zone.objects.filter(pk=zonePk).last()
                serializer = serializers.ZoneSerializer(zoneQuerySet)
                zoneData = serializer.data
                newZoneData = dict()
                newZoneData['pk'] = zoneData['pk']
                newZoneData['zone_name'] = zoneData['zone_name']
                newZoneData['zone_number'] = zoneData['zone_number']

                wrDict['work'] = newWorkData
                wrDict['secure'] = newSecureData
                wrDict['zone'] = newZoneData

                result.append(wrDict)
            
            

            return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def fetch_workingrecord_null_zone(self, request, village_pk, work_pk, date_str):
        """ Return all votetopics according to specific village """
        print(date_str)
        newdate = date_str.split("-")
        print(newdate[0])
        isExistWR = models.WorkingRecord.objects.filter(working_village=village_pk, working_work=work_pk,working_date__date=datetime.date(int(newdate[0]),int(newdate[1]),int(newdate[2]))).exists()
        if(isExistWR==False):
            return Response({ "detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
        else:
            workingRecord = models.WorkingRecord.objects.filter(working_village=village_pk, working_work=work_pk,working_date__date=datetime.date(int(newdate[0]),int(newdate[1]),int(newdate[2]))).values('working_secure','working_work').distinct()
            
            result = []

            for wr in workingRecord:
                # print(wr)
                wrDict = dict()

                workPk = wr['working_work']
                securePk = wr['working_secure']

                workQuerySet = models.Work.objects.filter(pk=workPk).last()
                serializer = serializers.WorkSerializer(workQuerySet)
                workData = serializer.data

                newWorkData = dict()
                newWorkData['pk'] = workData['pk']
                newWorkData['work_name'] = workData['work_name']

                secureQuerySet = models.SecureGuard.objects.filter(pk=securePk).last()
                serializer = serializers.SecureGuardSerializer(secureQuerySet)
                secureData = serializer.data
                newSecureData = dict()
                newSecureData['pk'] = secureData['pk']
                newSecureData['secure_firstname'] = secureData['secure_firstname']
                newSecureData['secure_lastname'] = secureData['secure_lastname']
                newSecureData['secure_type'] = secureData['secure_type']
                zonePk = secureData['secure_zone']

                zoneQuerySet = models.Zone.objects.filter(pk=zonePk).last()
                serializer = serializers.ZoneSerializer(zoneQuerySet)
                zoneData = serializer.data
                newZoneData = dict()
                newZoneData['pk'] = zoneData['pk']
                newZoneData['zone_name'] = zoneData['zone_name']
                newZoneData['zone_number'] = zoneData['zone_number']

                wrDict['work'] = newWorkData
                wrDict['secure'] = newSecureData
                wrDict['zone'] = newZoneData

                result.append(wrDict)
            
            

            return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def fetch_workingrecord_null_zone_null_work(self, request, village_pk, date_str):
        """ Return all votetopics according to specific village """
        print(date_str)
        newdate = date_str.split("-")
        print(newdate[0])
        isExistWR = models.WorkingRecord.objects.filter(working_village=village_pk,working_date__date=datetime.date(int(newdate[0]),int(newdate[1]),int(newdate[2]))).exists()
        if(isExistWR==False):
            return Response({ "detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
        else:
            workingRecord = models.WorkingRecord.objects.filter(working_village=village_pk,working_date__date=datetime.date(int(newdate[0]),int(newdate[1]),int(newdate[2]))).values('working_secure','working_work').distinct()
            
            result = []

            for wr in workingRecord:
                # print(wr)
                wrDict = dict()

                workPk = wr['working_work']
                securePk = wr['working_secure']

                workQuerySet = models.Work.objects.filter(pk=workPk).last()
                serializer = serializers.WorkSerializer(workQuerySet)
                workData = serializer.data

                newWorkData = dict()
                newWorkData['pk'] = workData['pk']
                newWorkData['work_name'] = workData['work_name']

                secureQuerySet = models.SecureGuard.objects.filter(pk=securePk).last()
                serializer = serializers.SecureGuardSerializer(secureQuerySet)
                secureData = serializer.data
                newSecureData = dict()
                newSecureData['pk'] = secureData['pk']
                newSecureData['secure_firstname'] = secureData['secure_firstname']
                newSecureData['secure_lastname'] = secureData['secure_lastname']
                newSecureData['secure_type'] = secureData['secure_type']
                zonePk = secureData['secure_zone']

                zoneQuerySet = models.Zone.objects.filter(pk=zonePk).last()
                serializer = serializers.ZoneSerializer(zoneQuerySet)
                zoneData = serializer.data
                newZoneData = dict()
                newZoneData['pk'] = zoneData['pk']
                newZoneData['zone_name'] = zoneData['zone_name']
                newZoneData['zone_number'] = zoneData['zone_number']

                wrDict['work'] = newWorkData
                wrDict['secure'] = newSecureData
                wrDict['zone'] = newZoneData

                result.append(wrDict)
            
            

            return notFoundHandling(result)


    @action(detail=True, methods = 'GET')
    def fetch_detailed_workingrecord(self, request, village_pk, zone_pk, work_pk, date_str, secure_pk):
        """ Return all votetopics according to specific village """
        print(date_str)
        newdate = date_str.split("-")
        print(newdate[0])
        isExistWR = models.WorkingRecord.objects.filter(working_village=village_pk, working_zone=zone_pk, working_work=work_pk,working_date__date=datetime.date(int(newdate[0]),int(newdate[1]),int(newdate[2])),working_secure=secure_pk).exists()
        if(isExistWR==False):
            return Response({ "detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
        else:
            workingRecord = models.WorkingRecord.objects.filter(working_village=village_pk, working_zone=zone_pk, working_work=work_pk,working_date__date=datetime.date(int(newdate[0]),int(newdate[1]),int(newdate[2])),working_secure=secure_pk).all()[::-1]
            serializer = serializers.WorkingRecordSerializer(workingRecord,many=True)
            workingRecordData = serializer.data

            result = []
            for wrData in workingRecordData:
                checkincheckpointPk = wrData['work_checkin_checkpoint']
                ccSet = models.CheckinCheckpoint.objects.filter(pk=checkincheckpointPk).last()
                serializer = serializers.CheckinCheckpointSerializer(ccSet)
                ccData = serializer.data

                wrData['checkpoint_name'] = ccData['point_name']
                wrData.pop('pk')
                wrData.pop('work_checkin_checkpoint')
                wrData.pop('working_village')
                wrData.pop('working_zone')
                wrData.pop('working_secure')
                wrData.pop('working_work')
                result.append(wrData)
  
            return notFoundHandling(result)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NotificationSerializer
    queryset = models.Notification.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    @action(detail=True, methods = 'GET')
    def get_unread_notification_count(self, request, user_pk):
        """ Return all votetopics according to specific village """
        user = models.GeneralUser.objects.only('pk').get(pk=user_pk)
    
        count = models.Notification.objects.filter(noti_general_user=user,noti_read_status=False).count()
        result = [count]
            # print(result)
        
        return notFoundHandling(result)

    @action(detail=True, methods = 'GET')
    def get_notification_generaluser_pk(self, request, user_pk):
        """ Return all votetopics according to specific village """
        user = models.GeneralUser.objects.only('pk').get(pk=user_pk)
    
        notification = models.Notification.objects.filter(noti_general_user=user).all()[::-1]
        serializer = serializers.NotificationSerializer(notification,many=True)
        notiData = serializer.data


        result =[]
        for noti in notiData:
            
            qrPk = noti['noti_qr']
            print(qrPk)

            qrcode = models.Qrcode.objects.filter(pk=qrPk).last()
            serializer = serializers.QrCodeSerializer(qrcode)
            qrcodeData = serializer.data
            
            qrDict = dict()
            qrDict['noti_pk'] = noti['pk']
            qrDict['qr_enter_time'] = qrcodeData['qr_enter_time']
            qrDict['qr_home_number'] = qrcodeData['qr_home_number']
            qrDict['qr_car_number'] = qrcodeData['qr_car_number']
            qrDict['qr_car_brand'] = qrcodeData['qr_car_brand']
            qrDict['qr_car_color'] = qrcodeData['qr_car_color']
            qrDict['noti_read_status'] = noti['noti_read_status']
            result.append(qrDict)

            # print(result)
        
        return notFoundHandling(result)

    @action(detail=True, methods=['post'])
    def create_enter_qrcode_and_notificaton(self, request):
        """ Create qr code on enter screen along with generate notification for each user"""
        
        data = request.data 

        isExistHome = models.Home.objects.filter(pk=data['qr_home'], is_active=True).exists()
        if(isExistHome==False):
            return Response({ "detail": "not have this home number "},status=status.HTTP_404_NOT_FOUND)
        else:
            home = models.Home.objects.filter(pk=data['qr_home'], is_active=True).last()
            serializer = serializers.HomeSerializer(home)
            homeData = serializer.data

            # print(homeData)


            ### using in qr code enter 
            homePk = homeData['pk']
            homeZone = homeData['home_zone']
            homeLat = homeData['home_lat']
            homeLon = homeData['home_lon']
            homeVillage = homeData['home_village']
            homeCompany = homeData['home_company']
            homeNumber = homeData['home_number']


            ### create enter qrcode 
            ### example models.Village.objects.only('pk').get(pk=village_pk)
            village = models.Village.objects.only('pk').get(pk=homeVillage)
            zone = models.Zone.objects.only('pk').get(pk=homeZone)
            company = models.Company.objects.only('pk').get(pk=homeCompany)
            home = models.Home.objects.only('pk').get(pk=homePk)
            secure = models.SecureGuard.objects.only('pk').get(pk=data['qr_enter_secure'])

            qrcode = models.Qrcode.objects.create(qr_enter_time=datetime.datetime.now(),qr_content=data['qr_content'], qr_type=data['qr_type'], qr_car_number=data['qr_car_number'],qr_home_number=homeNumber, qr_car_color = data['qr_car_color'], qr_car_brand=data['qr_car_brand'], qr_company = company, qr_village = village, qr_zone =zone, qr_home =home, qr_enter_secure=secure, qr_enter_status=True, qr_home_lat=homeLat,qr_home_lon= homeLon)
            qrcode.save
            serializer = serializers.QrCodeSerializer(qrcode)



            ## create notification 
            genUserQuerySet = models.GeneralUser.objects.filter(gen_user_home= home, is_active=True).all()
            for user in genUserQuerySet:
                print(user)
                notification = models.Notification.objects.create(noti_home=home,noti_general_user=user, noti_qr = qrcode)
                notification.save()

            ### for future, incase want to add secure warning
            # secureGuardQuerySet = models.SecureGuard.objects.filter(secure_zone= zone, is_active=True).all()
            # secureGuardSerializer = serializers.SecureGuardSerializer(secureGuardQuerySet, many=True)
            # secureGuardData = secureGuardSerializer.data

            # secure_list = []
            # for secure in secureGuardData:
            #     secure_list.append(secure['pk'])

            # print(secure_list)

            return Response(serializer.data,status.HTTP_201_CREATED)
        
       

    




# old views.

# class HelloApiView(APIView):
#     """ Test API View"""
#     serializers_class = serializers.HelloSerializer

#     def get(self, request, format=None):
#         """Return a list of APIView features"""

#         an_apiview = [
#             'Uses HTTP methods as functions (get, post, patch, put, delete)',
#             'Is similar to a traditional Django View',
#             'Gives you the most control over your logic',
#             'Is mapped manually to URLs',
#         ]

#         return Response({'message': 'Hello!', 'an_apiview': an_apiview})

#     def post(self,request):
#         """Create Hello message with our name"""
#         serializer = self.serializers_class(data=request.data)

#         if serializer.is_valid():
#             name = serializer.validated_data.get('name')
#             message = f'Hello {name}'
#             return Response({'message': message})
#         else:
#             return Response(
#                 serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST 
#             )

#     def put(self, request, pk=None):
#         """Handle update object (replace object)"""
#         return Response({'method':'PUT'})

#     def patch(self, request, pk=None):
#         """Handle partial update"""
#         return Response({'method':'PATCH'})

#     def delete(self, request, pk=None):
#         """Handle delete"""
#         return Response({'method':'DELETE'})


# class HelloViewSet(viewsets.ViewSet):
#     """Test API ViewSet"""
#     serializers_class = serializers.HelloSerializer

#     def list(self, request):
#         """Return a hello message."""

#         a_viewset = [
#             'Uses actions (list, create, retrieve, update, partial_update)',
#             'Automatically maps to URLS using Routers',
#             'Provides more functionality with less code',
#         ]

#         return Response({'message': 'Hello!', 'a_viewset': a_viewset})

#     def create(self, request):
#         """Create a new hello message."""
#         serializer = self.serializer_class(data=request.data)

#         if serializer.is_valid():
#             name = serializer.validated_data.get('name')
#             message = f'Hello {name}!'
#             return Response({'message': message})
#         else:
#             return Response(
#                 serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#     def retrieve(self, request, pk=None):
#         """Handle getting an object by its ID"""

#         return Response({'http_method': 'GET'})

#     def update(self, request, pk=None):
#         """Handle updating an object"""

#         return Response({'http_method': 'PUT'})

#     def partial_update(self, request, pk=None):
#         """Handle updating part of an object"""

#         return Response({'http_method': 'PATCH'})

#     def destroy(self, request, pk=None):
#         """Handle removing an object"""

#         return Response({'http_method': 'DELETE'})





# class UserProfileFeedViewSet(viewsets.ModelViewSet):
#     authentication_classes = (TokenAuthentication,)
#     ## every time http request, pass to serializer and call.save() then passto perform_created
#     serializer_class = serializers.ProfileFeedItemSerializer 
#     queryset = models.ProfileFeedItem.objects.all()
#     permission_classes = (
#         permission.UpdatedOwnStatus,
#         IsAuthenticatedOrReadOnly
#     )
    
#     def perform_create(self, serializer): ## do every time creaet http post request to our we set, to create
#         """Set the user profile to the logged in user, to create custom object model"""
#         ## request is parameter that come with self every time that have request 
#         ## .user can use when use "authentication_classes = (TokenAuthentication,)". 
#         serializer.save(user_profile=self.request.user)




    