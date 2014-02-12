__author__ = 'cr'

import select
import socket

import settings
bufferSize = 1024  # whatever you need

print("Starting server")
print("UDP target IP:", settings.LOG_SERVER_IP)
print("UDP target port:", settings.LOG_SERVER_PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((settings.LOG_SERVER_IP, settings.LOG_SERVER_PORT))
s.setblocking(0)

while True:
    result = select.select([s], [], [])
    msg = result[0][0].recv(bufferSize)
    print msg