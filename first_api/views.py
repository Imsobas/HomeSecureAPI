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
# from django.core.serializers.json import DjangoJSONEncoder
# from django.core import serializers 

from first_api import serializers 
from first_api import models
from first_api import permission
import json


# Home Secure main views 

class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = models.Company.objects.all() ## if not change this, get wrong url 
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class VillageViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VillageSerializer
    queryset = models.Village.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, permission.UpdateAllVillage,)

    def list(self, request):
        """Return all Village"""
        villages = {village.village_name: village.id for village in models.Village.objects.all()}
        print(villages)
        print(type(villages))

        return Response(villages)   

class ZoneViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ZoneSerializer
    queryset = models.Zone.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    ## return a zone of that village
    def retrieve(self, request, pk):
        """Return all zone according to that village id"""
        
        # zones = {
        #     "id": zone.id,
        #     "zone_name": zone.zone_name,
        #     "zone_" : zone.zone_village,
        #     "zone.zone_lat" : zone.zone_lat,
        #     "zone.zone_lon" : zone.zone_lon,
        #     "zone.zone_last_update" : zone.zone_last_update for zone in models.Zone.objects.filter(zone_village = pk)
        # }
        
        ##mrthod 1
        # serialized_q = models.Zone.objects.filter(zone_village = pk).values()
        # query = json.dumps(list(serialized_q), cls=DjangoJSONEncoder)
        ## ans: get str wiht \

        ##method2
        # objectQuerySet = models.Zone.objects.filter(zone_village = pk)
        # data = djangoSerializers.serialize('json', list(objectQuerySet),fields =)
        
        
        ##method3
        # jsonSerializer = json.dumps(list(objectQuerySet), cls=DjangoJSONEncoder)

        ##method 4 ## work 
        zone_by_village = list(models.Zone.objects.filter(zone_village = pk).values())
        
        if(len(zone_by_village)>0):
            return Response(zone_by_village)
        else:
            return Response(
                { "detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )

            
        
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
    permission_classes = (permission.UpdateOwnProfile,)


# old views.

class HelloApiView(APIView):
    """ Test API View"""
    serializers_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Return a list of APIView features"""

        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self,request):
        """Create Hello message with our name"""
        serializer = self.serializers_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST 
            )

    def put(self, request, pk=None):
        """Handle update object (replace object)"""
        return Response({'method':'PUT'})

    def patch(self, request, pk=None):
        """Handle partial update"""
        return Response({'method':'PATCH'})

    def delete(self, request, pk=None):
        """Handle delete"""
        return Response({'method':'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializers_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message."""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLS using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message."""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""

        return Response({'http_method': 'DELETE'})





class UserProfileFeedViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    ## every time http request, pass to serializer and call.save() then passto perform_created
    serializer_class = serializers.ProfileFeedItemSerializer 
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permission.UpdatedOwnStatus,
        IsAuthenticatedOrReadOnly
    )
    
    def perform_create(self, serializer): ## do every time creaet http post request to our we set, to create
        """Set the user profile to the logged in user, to create custom object model"""
        ## request is parameter that come with self every time that have request 
        ## .user can use when use "authentication_classes = (TokenAuthentication,)". 
        serializer.save(user_profile=self.request.user)




    