from django.shortcuts import render
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import Connection

from messages.models import Message
from messages.serializers import MessageSerializer


def message_log(request):
    context = {}
    return render(request, 'messages/index.html', context)

@csrf_exempt
@api_view(['GET'])
def messages(request):
   #connect to our local mongodb
    db = Connection('localhost', 27017)
    #get a connection to our database
    dbconn = db['tdlogger']
    messagesCollection = dbconn['messages']

    if request.method == 'GET':
        #get our collection
        messages = []
        for r in messagesCollection.find():
            restaurant = Message(r["_id"], r["timestamp"], r["level"], r["source"], r["message"])
            messages.append(restaurant)
        serializedList = MessageSerializer(messages, many=True)
        return Response(serializedList.data)
    else:
        return Response({"ok": "false"})


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.using('mongodb').all()
    serializer_class = MessageSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'


