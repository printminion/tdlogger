"""It does cool things"""

import sys
import json
import inspect
import datetime

from socket import *
from tdlogger import metadata


__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright


class tdlogger:
    _SOURCE = None
    _LOG_SERVER_IP = None
    _LOG_SERVER_PORT = None

    _LOG_LEVEL_INFO = 'info'
    _LOG_LEVEL_WARN = 'warning'
    _LOG_LEVEL_EXCEPTION = 'exception'

    session = None

    def __init__(self, source, server, ip):
        self._SOURCE = source
        self._LOG_SERVER_IP = server
        self._LOG_SERVER_PORT = ip

    def _log(self, source, level, message, msgFull=None):
        frame, filename, line_number, function_name, lines, index = \
            inspect.getouterframes(inspect.currentframe())[2]

        cs = socket(AF_INET, SOCK_DGRAM)
        cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        MESSAGE = {'timestamp': str(datetime.datetime.utcnow()),
                   'source': source,
                   'level': level,
                   'message': message,
                   'filename': filename,
                   'line_number': line_number,
                   'session': self.session,
                   'payload': msgFull
                   }

        try:
            obj = json.dumps(MESSAGE)
            #obj = cPickle.dumps(MESSAGE) #53 bytes more than json object

            cs.sendto(obj, (self._LOG_SERVER_IP, self._LOG_SERVER_PORT))
        except:
            print "exception", sys.exc_info()[0]

    def info(self, msg, msgFull=None):
        self._log(self._SOURCE, self._LOG_LEVEL_INFO, msg, msgFull)

    def warning(self, msg, msgFull=None):
        self._log(self._SOURCE, self._LOG_LEVEL_WARN, msg, msgFull)

    def exception(self, msg, msgFull=None):
        self._log(self._SOURCE, self._LOG_LEVEL_EXCEPTION, msg, msgFull)
