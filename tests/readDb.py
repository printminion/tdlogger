#!/usr/bin/env python

import json
import datetime

__author__ = 'cr'

import select
import socket

import settings
from pymongo import MongoClient
#from bson.objectid import ObjectId
from bson.son import SON

bufferSize = 1024  # whatever you need

client = MongoClient(settings.LOG_SERVER_DB_HOST, settings.LOG_SERVER_DB_PORT)
db = client[settings.LOG_SERVER_DB_NAME]

messages = db.messages

print "[i]get one message: %s" % \
      messages.find_one()

print "[i]count all messages: %s" % \
      messages.count()

print "[i]get one error: %s" % \
      messages.find_one({'level': 1})

print "[i]count messages by type: %s" % \
      messages.find({'level': 1}).count()


print "[i]get messages for specific day:"

d = datetime.datetime(2014, 2, 15)
for message in messages.find({"timestamp": {"$gte": d}, "source": "host1"}).sort("timestamp"):
    print message

# def get(post_id):
#     # Convert from string to ObjectId:
#     document = client.db.collection.find_one({'_id': ObjectId(post_id)})

#print "count by errors"
# db.messages.aggregate([
#     {"$match": "$level"},
#     {"$group": {"_id": "$level", "count": {"$sum": 1}}}
#     #, {"$sort": SON([("count", -1), ("_id", -1)])}
# ])

print "[i]get messages by user:"
for message in messages.find({"source": "host1", "payload.user_id": 1111111}).sort("timestamp"):
    print message

print "[i]get messages by session:"
for message in messages.find({"source": "host1", "session.session_id": 'cda84c2176977ee3b012b49f1cec2511'})\
        .sort("timestamp"):
    print message


print "[i]count states by host:"
db.messages.aggregate([
    {"$match": "level"},
    {"$group": {"_id": "level", "count": {"$sum": 1}}}
    #, {"$sort": SON([("count", -1), ("_id", -1)])}
])


def getMessages(data):

    messages = db.messages
    post_id = messages .insert(data)
    return post_id

print "[i]show collections: %s" % \
    db.collection_names()

#print '[>]%s messages' % len(msg)



