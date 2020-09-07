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
        

# Home Secure main views 

class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = models.Company.objects.all()
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

class QrCodeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.QrCodeSerializer
    queryset = models.Qrcode.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods = 'GET')
    def get_qrcodes_homedetails(self, request, number):

        currentQuerySet = models.Home.objects.filter(home_number=number, is_active=True).all()
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
        querySet = models.Qrcode.objects.filter(qr_village=village_pk, is_active=True, qr_inside_status=False).all()
        serializer = serializers.QrCodeSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)

    ## qr_user_screen_services
    @action(detail=True, methods = 'GET')
    def get_villages_pk_homes_pk_qrcodes(self, request, village_pk, home_pk):
        """ Return all information specific to qr_user_services """
        querySet = models.Qrcode.objects.filter(qr_village=village_pk, qr_home=home_pk, is_active=True, qr_home_status=False).all()
        serializer = serializers.QrCodeSerializer(querySet,many=True)
        result = serializer.data
            
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

    ## qr_history_screen_services
    @action(detail=True, methods = 'GET')
    def get_villages_pk_maintenance_fee_period(self, request, village_pk):
        """ Return all qr codeinformation specific for qr history list service """
        querySet = models.MaintenanceFeePeriod.objects.filter(fee_village=village_pk,is_active=True).all()
        serializer = serializers.MaintenanceFeePeriodSerializer(querySet,many=True)
        result = serializer.data
            
        return notFoundHandling(result)

class MaintenanceFeeRecordViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MaintenanceFeeRecordSerializer
    queryset = models.MaintenanceFeeRecord.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    ## qr_history_screen_services
    @action(detail=True, methods = 'GET')
    def get_maintenance_fee_period_pk_maintenance_fee_record(self, request, pk):
        """ Return all maintenance fee record according to specific village and maintenance"""
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




    