from rest_framework import viewsets,permissions,status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from events.serializers import EventSerializer,GetEventSerializer
from events.models import Event
from profiles.models import Profile
from collectionsNft.models import Collection
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

"""--------------------------Events---------------------------"""
#1 view -> allow to create a Room
class EventViewSet(viewsets.ModelViewSet):
  queryset = Event.objects.all()  
  permission_classes = (permissions.IsAuthenticated, )
  def create(self, request):
    user = self.request.user
    try:
      collection_id = request.data['collection']
      collection = Collection.objects.get(id=collection_id)
      if user == collection.creator.user:
        request.data['creator'] = collection.creator.id
        newEvent = EventSerializer(data=request.data)
        if newEvent.is_valid():
          newEvent.save()
          return Response(newEvent.data,status = status.HTTP_201_CREATED)
        else:
          return Response(newEvent.error, status=status.HTTP_400_BAD_REQUEST)
      else:
        return Response({"Error":"User not allowed"}, status=status.HTTP_403_FORBIDDEN)
    except:
      return Response({"Error":"Error occured while creating the room"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  def update(self, request, pk=None):
    response = {'message': 'Update function is not offered in this path.'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)

  def partial_update(self, request, pk=None):
    response = {'message': 'Update function is not offered in this path.'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)

  def destroy(self, request, pk=None):
    response = {'message': 'Delete function is not offered in this path.'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)
  
  def list(self,request):
    response = {'message': 'List function is not offered in this path.'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)

#2 view -> Retrieve Events for a specific collection / address
class GetEventView(ListAPIView):
  permission_classes = (permissions.IsAuthenticated,)
  serializer_class = GetEventSerializer
  def get(self,request):
    return Response({"Error":"Wrong request"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
  
  def post(self,request):
    paginator = PageNumberPagination()
    paginator.page_size = 150
    try:
      if request.data['address']:        
        events = Event.objects.filter(addresses__contains=request.data['address'])              
        if request.data['collectionId'] != "None":
          try:
            collectionId = request.data['collectionId']   
            collection = Collection.objects.get(id=collectionId)
            events = events.filter(collection=collection)
          except:
            return Response({"Error":"Wrong collection data"}, status=status.HTTP_400_BAD_REQUEST)
          
        result_page = paginator.paginate_queryset(events, request)
        postsSerialized = GetEventSerializer(events,many=True)
        return paginator.get_paginated_response(postsSerialized.data)
      else:
        return Response({"Error":"Wrong address field"}, status=status.HTTP_400_BAD_REQUEST)
    except:
      return Response({"Error":"Wrong address field"}, status=status.HTTP_400_BAD_REQUEST)


  
#3 view -> Claim Event 
class ClaimEventAccessView(APIView):
  serializer_class = EventSerializer
  permission_classes = [permissions.IsAuthenticated]
    
  def post(self, request, format=None):
    user = self.request.user
    try:
      if request.data['address'] and request.data['roomId']:
        try:
          event = Event.objects.get(id=int(request.data['roomId']))
          if request.data['address'] in event.addresses:
            try:
              """
              email = EmailMessage(
                'Apokl - Your exclusive room access ',
                f'Welcome {user.username}, you have access to {room.title}. More about this : {room.content}',
                'guillaumedesurville99@gmail.com',
                [user.email],
                headers={'Message-ID': 'foo'},
              )
              email.send()
              """
              to = user.email
              picture = event.collection.picture
              creator = event.creator.name
              print(creator,picture)
              html_content = render_to_string("room_email_template.html",
                                {'collectionImage':picture,
                                  'roomName':event.title,
                                  'content':event.content,
                                  'user':user.username,
                                  'creatorName':creator})
              text_content = strip_tags(html_content)
              index = event.addresses.index(request.data['address'])
              email = EmailMultiAlternatives(
                #subject : 
                "Apokl - Acces exclusive event",
                #content : 
                text_content,
                #from email
                settings.EMAIL_HOST_USER,
                #to:
                [to]                
              )
              email.attach_alternative(html_content,"text/html")
              email.send()

              event.addresses.pop(index)
              event.users.append(user.username)
              event.save(update_fields=['addresses','users'])
              return Response({'success': 'Message sent successfully'})
            except:
              return Response({'error': 'Message failed'}, status=status.HTTP_400_BAD_REQUEST)
          else:
            return Response({'error': 'User not allowed'}, status=status.HTTP_400_BAD_REQUEST)
        except:
          return Response({"error":"No collection corresponding"}, status=status.HTTP_400_BAD_REQUEST)
      else:
        return Response({"Error":"Collection is not specified"}, status=status.HTTP_400_BAD_REQUEST)    
    except:
      return Response({"Error":"Missing fields"}, status=status.HTTP_400_BAD_REQUEST)    
    
    
    

