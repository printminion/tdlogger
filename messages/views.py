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


@csrf_exempt
@api_view(['GET'])
def tclogger_status(request):
    """
        get messages count since date
    """

    if request.method != 'GET':
        return Response({"ok": "false"})

    #connect to mongodb
    db = Connection(settings.LOG_SERVER_DB_HOST, settings.LOG_SERVER_DB_PORT)
    dbconn = db[settings.LOG_SERVER_DB_NAME]

    messagesCollection = dbconn['messages']

    #count = messagesCollection.find({"timestamp": {"$gte": d}}).count()

    FINAL_DATE = datetime.datetime.now()
    last6_hours = datetime.timedelta(hours=6)
    INITIAL_DATE = FINAL_DATE - last6_hours
    SOURCE = 'host1'

    # result = messagesCollection.aggregate(
    #     {'$match': {'timestamp': {'$gte': INITIAL_DATE, '$lt': FINAL_DATE, 'source': SOURCE}}},
    #     {'$group': {'_id': {'hour': "$hour"}, 'queriesPerHost': {'$sum:' "$count"}}}
    # )

    #,{'$group': {'_id': {'hour': "$hour"}, 'queriesPerHost': {'$sum:' "$count"}}}

    result = messagesCollection.aggregate([
        #{'$match': {'timestamp': {'$gte': INITIAL_DATE, '$lt': FINAL_DATE}}}
        #{'$match': {'timestamp': {'$lt': FINAL_DATE}}}
        {'$match': {'timestamp': {'$gte': INITIAL_DATE}}}
        , {'$group': {'_id': {'hour': "$hour"}, 'queriesPerHost': {'$sum': 1}}}
    ])


    #create array grouped by time
    groupedByTime = {}
    for time in result['result']:
        groupedByTime['%s:00' % time['_id']['hour']] = time['queriesPerHost']

    times = ['time', '00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00'
            , '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00'
            , '20:00', '21:00', '22:00', '23:00'
            ]

    payload = []
    for time in times:
        if groupedByTime.has_key(time):
            payload.append([time, groupedByTime[time]])
        else:
            value = ''
            if time != 'time':
                value = 0
            payload.append([time, value])

    status = {}
    #count total messages
    status['total'] = '%s' % messagesCollection.find().count()

    last10_minutes = datetime.timedelta(minutes=6)
    INITIAL_DATE = FINAL_DATE - last10_minutes

    #count messages in last 10 minutes
    result = messagesCollection.find({'timestamp': {'$gte': INITIAL_DATE}}).count()
    status['last10minutes'] = '%s' % result
    status['messages'] = payload

    return Response({'payload': status, 'ok': 'true'})


class MessageViewSet(viewsets.ModelViewSet):
    """
    does not work yet
    """
    queryset = Message.objects.using('mongodb').all()
    serializer_class = MessageShortSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'


