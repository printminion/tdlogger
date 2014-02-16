import datetime
import json
import settings
from bson import ObjectId
from django.shortcuts import render
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import Connection

from messages.models import Message
from messages.serializers import MessageShortSerializer
from messages.serializers import MessageFullSerializer


def message_log(request):
    context = {}
    return render(request, 'messages/index.html', context)


@csrf_exempt
@api_view(['GET'])
def message_list(request):
    #connect to mongodb
    db = Connection(settings.LOG_SERVER_DB_HOST, settings.LOG_SERVER_DB_PORT)
    dbconn = db[settings.LOG_SERVER_DB_NAME]

    messagesCollection = dbconn['messages']

    if request.method != 'GET':
        return Response({"ok": "false"})

    messages = []
    for m in messagesCollection.find().sort([("timestamp", -1)]):
        message = Message(
        m["_id"]
        , m["timestamp"]
        , m["level"]
        , m["source"]
        , m["message"]
        )
        messages.append(message)
    serializedList = MessageShortSerializer(messages, many=True)
    return Response(serializedList.data)


@csrf_exempt
@api_view(['GET'])
def message_detail(request, pk):
    db = Connection(settings.LOG_SERVER_DB_HOST, settings.LOG_SERVER_DB_PORT)
    dbconn = db[settings.LOG_SERVER_DB_NAME]

    messagesCollection = dbconn['messages']

    if request.method != 'GET':
        return Response({"ok": "false"})

    messages = []

    for m in messagesCollection.find({'_id': ObjectId(pk)}):
        message = Message(
            m["_id"]
            , m["timestamp"]
            , m["level"]
            , m["source"]
            , m["message"]
            , m["filename"]
            , m["line_number"]
            , m["session"]
            , m["payload"]
        )
        messages.append(message)
    serializedList = MessageFullSerializer(messages, many=True)
    return Response(serializedList.data)


@csrf_exempt
@api_view(['POST'])
def messages_since(request):
    """
        get messages count since date
    """

    if request.method != 'POST':
        return Response({"ok": "false"})

    if request._content_type != 'application/json':
        return Response({"ok": "false"})


    try:
        content = json.loads(request._post['_content'])
        print content
        since = content['since']
        print since

        d = datetime.datetime.fromtimestamp(since / 1e3)
    except:
        return Response({"ok": "false"})

    #connect to mongodb
    db = Connection(settings.LOG_SERVER_DB_HOST, settings.LOG_SERVER_DB_PORT)
    dbconn = db[settings.LOG_SERVER_DB_NAME]

    messagesCollection = dbconn['messages']

    #count = messagesCollection.find({"timestamp": {"$gte": d}, "source": "host1"}).count()
    count = messagesCollection.find({"timestamp": {"$gte": d}}).count()
    return Response({'payload': count, 'ok': 'true'})


class MessageViewSet(viewsets.ModelViewSet):
    """
    does not work yet
    """
    queryset = Message.objects.using('mongodb').all()
    serializer_class = MessageShortSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'


