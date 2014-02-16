#!/usr/bin/env python

import json
import select
import socket

import settings
from pymongo import MongoClient
from bson import json_util

bufferSize = 1024  # whatever you need

print("Starting ndlogger daemon")
print("UDP target IP:", settings.LOG_SERVER_IP)
print("UDP target port:", settings.LOG_SERVER_PORT)

#start
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((settings.LOG_SERVER_IP, settings.LOG_SERVER_PORT))
s.setblocking(0)

client = MongoClient(settings.LOG_SERVER_DB_HOST, settings.LOG_SERVER_DB_PORT)
db = client[settings.LOG_SERVER_DB_NAME]


def addToDB(data):

    messages = db.messages
    post_id = messages.insert(data)
    return post_id

while True:
    result = select.select([s], [], [])
    msg = result[0][0].recv(bufferSize)
    #print '%s ----> %s' % (len(msg), msg)
    print '[>]%s bytes' % len(msg)

    data = json.loads(msg, object_hook=json_util.object_hook)  # here we can loose time


    data['hour'] = data['timestamp'].hour

    print '[%s]%s\t%s' % (data['level'][0:1], data['timestamp'], data['message'])

    post_id = addToDB(data)
    print '[<]added to db:%s' % post_id




