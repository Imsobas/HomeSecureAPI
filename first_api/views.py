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


    @action(detail=True, methods=['post'])
    def testObservation(self, request):
        """ Test def"""
        data = request.data
        try:
            print(data['observation_date'])
            pointObservation = models.PointObservation.objects.only('pk').get(observation_village=data['observation_village'], observation_zone=data['observation_zone'], observation_work=data['observation_work'], observation_secure=data['observation_secure'], observation_date=data['observation_date'])
        except models.PointObservation.DoesNotExist:
            print("except case")

            village = models.Village.objects.only('pk').get(pk=data['observation_village'])
            zone = models.Zone.objects.only('pk').get(pk=data['observation_zone'])
            work = models.Work.objects.only('pk').get(pk=data['observation_work'])
            secure = models.SecureGuard.objects.only('pk').get(pk=data['observation_secure'])

            pointObservation = models.PointObservation.objects.create(observation_village=village, observation_zone=zone, observation_work=work, observation_secure=secure)
            pointObservation.save()
        
        try:
            pointObservationRecord = models.PointObservationRecord.objects.only('pk').get(observation_pk=pointObservation, observation_timeslot=data['observation_timeslot'],checkpoint_pk = data['checkpoint_pk'])
            return Response({ "detail": 'already have this point observation record'},status=status.HTTP_200_OK)
            
        except models.PointObservationRecord.DoesNotExist:
            checkpoint = models.Checkpoint.objects.only('pk').get(pk=data['checkpoint_pk'])
            pointObservationRecord = models.PointObservationRecord.objects.create(observation_checkin_time=data['observation_checkin_time'], observation_checkout_time=data['observation_checkout_time'],observation_timeslot=data['observation_timeslot'],checkpoint_pk = checkpoint, observation_pk= pointObservation )

            pointObservationRecord.save()

            serializer = serializers.PointObservationRecordSerializer(pointObservationRecord)

            return Response(serializer.data,status.HTTP_201_CREATED)

        # village = models.Village.objects.only('pk').get(pk=data['observation_village'])
        # # village = models.PointObservation.objects.filter(pk=data['observation_village'])   # comment = Comment.objects.filter(pk=comment_id)
        # print(village)
        # new_test = models.PointObservation.objects.create(observation_village=village,observation_hour_split=data['observation_hour_split'])
        # new_test.save()

        # serializer = serializers.PointObservationSerializer(new_test)
        
        ### get new pk model again after create model
        # new_test = models.PointObservation.objects.only('pk').get(observation_village=village,observation_hour_split=data['observation_hour_split'])
        # print(new_test)

        

        # serializer = serializers.PointObservationSerializer(data=request.data)
        # print(serializer.data['observation_village'])
        # if serializer.is_valid():
        #     print(serializer.data['observation_village'])
        # else:
        #       return Response({ "detail": error_message},status=status.HTTP_404_NOT_FOUND)
      




class PointObservationPointListViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PointObservationPointListSerializer
    queryset = models.PointObservationPointList.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class PointObservationRecordViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PointObservationRecordSerializer
    queryset = models.PointObservationRecord.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

# class PointInspectionViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.PointInspectionSerializer
#     queryset = models.PointInspection.objects.all()
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)

            
        



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




    