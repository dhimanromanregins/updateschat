from django.shortcuts import render
from .models import Room, Message
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room, Contact
from .serializers import RoomSerializer, MessageSerializer, ContactSerializer
from django.http import Http404
from django.db.models import Q
from collections import defaultdict


def rooms(request):
    rooms=Room.objects.all()
    return render(request, "rooms.html",{"rooms":rooms})

def room(request,slug):
    try:
        room_name=Room.objects.get(slug=slug).name
        messages=Message.objects.filter(room=Room.objects.get(slug=slug))
        return render(request, "room.html",{"room_name":room_name,"slug":slug,'messages':messages})
    except:
        return render(request, "room.html")
class RoomList(APIView):
    """
    List all rooms or create a new room.
    """
    def get(self, request, format=None):
        response = {'status': False}
        room_name = request.GET.get('room_name', None)
        reverse_room_name = room_name.split('_chat_')[1] + '_chat_' + room_name.split('_chat_')[0]
        if room_name:
            messages = Message.objects.filter(Q(room__name=room_name) | Q(room__name=reverse_room_name))
            message_data = MessageSerializer(messages, many=True).data
            response['status'] = True
            response['message_data'] = message_data
        return Response(response)

    def post(self, request, format=None):
        # Deserialize the request data using your RoomSerializer
        print('request.data>>>>', request.data)
        serializer = RoomSerializer(data=request.data)

        if serializer.is_valid():
            room_name = serializer.validated_data['name']
            reverse_room_name = room_name.split('_chat_')[1] + '_chat_' + room_name.split('_chat_')[0]
            room_slug = serializer.validated_data['slug']

            # Check if a room with the same name or slug already exists
            if Room.objects.filter(Q(name=room_name) | Q(name=reverse_room_name)).exists():
                # Retrieve the first hundred messages based on the slug
                messages = Message.objects.filter(room__slug=room_slug)[:100]
                message_data = MessageSerializer(messages, many=True).data


                # Create the response data with the error message and messages
                response_data = {
                    "detail": "Room and slug already exist",
                    "messages": message_data
                }

                return Response(response_data, status=status.HTTP_201_CREATED)

            # Save the new room
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class RoomDetail(APIView):
    """
    Retrieve, update or delete a room instance.
    """
    def get_object(self, slug):
        try:
            return Room.objects.get(slug=slug)
        except Room.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        room = self.get_object(slug)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        room = self.get_object(slug)
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        room = self.get_object(slug)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContactsList(APIView):
    def get(self, request, format=None):
        response = {'status': False}
        user_id = request.GET.get('user_id', None)
        if user_id:
            contacts = Contact.objects.filter(user_id=user_id)
            contact_data = ContactSerializer(contacts, many=True).data
            response['status'] = True
            response['contact_data'] = contact_data
        return Response(response)