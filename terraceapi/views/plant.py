# AUTHOR: JARON LANE

"""View module for handling requests about posts"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from terraceapi.models import Plant, Location
from django.contrib.auth.models import User
import datetime

class Plant(ViewSet):
    """Terrace Plants"""

    def create(self, request):
        """Handle POST operations for plants

        Returns:
            Response -- JSON serialized event instance
        """
        user = User.objects.get(user=request.auth.user)
        location = Location.objects.get(pk=request.data["location_id"])
        

        plant = Plant()
        plant.user = user
        plant.title = request.data["title"]
        plant.nick_name = request.data["nick_name"]
        plant.location = location
        plant.about = request.data["about"]
        plant.watering_frequency = request.data["watering_frequency"]
        plant.date_watered = datetime.datetime.now()


        try:
            plant.save()
            serializer = PlantSerializer(plant, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized game instance
        """
        user = User.objects.get(user=request.auth.user)


        try:
            plant = Plant.objects.get(pk=pk)
            if user.id == plant.user_id: 
                plant.is_current_user = True
            else:
                plant.is_current_user = False
            serializer = PlantSerializer(plant, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        user = User.objects.get(user=request.auth.user)
        location = Location.objects.get(pk=request.data["location_id"])
        

        plant = Plant()
        plant.user = user
        plant.title = request.data["title"]
        plant.nick_name = request.data["nick_name"]
        plant.location = location
        plant.about = request.data["about"]
        plant.watering_frequency = request.data["watering_frequency"]
        plant.date_watered = datetime.datetime.now()
        
        plant.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
   
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a post
            Created By: Jake Butler
            Date: 2/24/21
            Subject: Defines server response for deleting posts
        

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            plant = Plant.objects.get(pk=pk)
            plant.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Plant.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to post resource

        Returns:
            Response -- JSON serialized list of posts
        """
        plants = Plant.objects.all()

        serializer = PlantSerializer(
            plants, many=True, context={'request': request})
        return Response(serializer.data)