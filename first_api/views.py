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

    @action(detail=True, methods = 'GET')
    def get_qrcodes_homedetails(self, request, number):

        currentQuerySet = models.Home.objects.filter(home_number=number, is_active=True).all()
        currentSerializer = serializers.HomeSerializer(currentQuerySet,many=True)
        currentData =  currentSerializer.data

        result = []
        
        home_dict = dict()
        for home in currentData:
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
        

        if(len(result)!=1 ):
            return Response({ "detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
        if(len(result)>1 ):
            return Response({ "detail": "Error, multiple home"},status=status.HTTP_404_NOT_FOUND)
       
        return notFoundHandling(home_dict)
            






            
        



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




    