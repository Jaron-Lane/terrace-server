# AUTHOR: JARON LANE

"""View module for handling requests about locations"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from terraceapi.models import Location
from django.contrib.auth.models import User
import datetime

class Locations(ViewSet):
    """Terrace Locations"""

    def create(self, request):
        """Handle POST operations for locations

        Returns:
            Response -- JSON serialized location instance
        """
        user = request.auth.user
        
        location = Location()
        location.user = user
        location.name = request.POST.get("name")
        location.lighting = request.POST.get("lighting")
        location.photo = request.FILES.get("photo")

        try:
            location.save()
            serializer = LocationSerializer(location, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single location

        Returns:
            Response -- JSON serialized location instance
        """
        user = request.auth.user

        try:
            location = Location.objects.get(pk=pk)
            if user.id == location.user_id: 
                location.is_current_user = True
            else:
                location.is_current_user = False
            serializer = LocationSerializer(location, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        user = request.auth.user

        location = Location.objects.get(pk=pk)
        location.user = user
        location.name = request.data["name"]
        location.lighting = request.data["lighting"]
        location.photo = request.FILES.get("photo")
        
        location.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
   
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a location
            
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            location = Location.objects.get(pk=pk)
            location.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Location.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to post resource

        Returns:
            Response -- JSON serialized list of posts
        """
        locations = Location.objects.filter(user = request.auth.user)

        # .order_by('-publication_date') => THIS IS A COOL TRICK TO REMEMBER FOR THE FUTURE

        serializer = LocationSerializer(
            locations, many=True, context={'request': request})
        return Response(serializer.data)

class LocationSerializer(serializers.ModelSerializer):
    """JSON serializer for locations

    Arguments:
        serializer type
    """
    class Meta:
        model = Location
        fields = ('id', 'user', 'name', 'lighting', 'photo')
        depth = 1