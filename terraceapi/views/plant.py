import datetime
import time
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from terraceapi.models import Plant, Location

class Plants(ViewSet):
    """Terrace Plants"""
    def add_on_days(self, date, num):
        ret = time.strftime("%Y-%m-%d",time.localtime(time.mktime(time.strptime(str(date),"%Y-%m-%d"))+num*3600*24+3600))      
        return ret

    def create(self, request):
        """Handle POST operations for plants

        Returns:
            Response -- JSON serialized event instance
        """
        user = request.auth.user
        location = Location.objects.get(pk=request.data["location_id"])
        

        plant = Plant()
        plant.user = user
        plant.title = request.data["title"]
        plant.nick_name = request.data["nick_name"]
        plant.location = location
        plant.about = request.data["about"]
        plant.watering_frequency = request.data["watering_frequency"]
        plant.date_watered = datetime.date.today()


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
        user = request.auth.user


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
        user = request.auth.user
        location = Location.objects.get(pk=request.data["location_id"])
        

        plant = Plant.objects.get(pk=pk)
        plant.user = user
        plant.title = request.data["title"]
        plant.nick_name = request.data["nick_name"]
        plant.location = location
        plant.about = request.data["about"]
        plant.watering_frequency = request.data["watering_frequency"]
        plant.date_watered = datetime.date.today()
        
        plant.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
   
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a post

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


    @action(methods=["get"], detail=True)
    def water(self, request, pk=None):
        plant = Plant.objects.get(pk=pk)
        plant.date_watered = datetime.date.today()
        plant.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """Handle GET requests to post resource

        Returns:
            Response -- JSON serialized list of posts
        """
        plants = Plant.objects.filter(user=request.auth.user)

        plants_due = []

        todays_plants = self.request.query_params.get('todays_plants', None)
        if todays_plants is not None:

            for plant in plants:
                due_date = self.add_on_days(plant.date_watered, plant.watering_frequency)
                date_object = datetime.datetime.strptime(due_date, '%Y-%m-%d').date()

                if date_object == datetime.date.today() or date_object < datetime.date.today():
                    plants_due.append(plant)
            serializer = PlantSerializer(
                plants_due, many=True, context={'request': request}) 
        else:
            serializer = PlantSerializer(
                plants, many=True, context={'request': request})
                
        return Response(serializer.data)

class PlantSerializer(serializers.ModelSerializer):
    """JSON serializer for plants

    Arguments:
        serializer type
    """
    class Meta:
        model = Plant
        fields = ('id', 'user',  'title', 'nick_name', 'location', 'about', 'watering_frequency', "date_watered", 'is_current_user')
        depth = 1