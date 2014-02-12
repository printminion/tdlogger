"""It does cool things"""

from tdlogger import metadata


__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright

import inspect
from socket import *


class tdlogger:
    _HOST = None
    _LOG_SERVER_IP = None
    _LOG_SERVER_PORT = None

    _LOG_LEVEL_INFO = 1
    _LOG_LEVEL_WARN = 2
    _LOG_LEVEL_FATAL = 3

    def __init__(self, host, server, ip):
        self._HOST = host
        self._LOG_SERVER_IP = server
        self._LOG_SERVER_PORT = ip

    def _log(self, host, level, msg, msgFull=None):
        frame, filename, line_number, function_name, lines, index = \
            inspect.getouterframes(inspect.currentframe())[2]

        cs = socket(AF_INET, SOCK_DGRAM)
        cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        MESSAGE = "%s|%s|%s|%s|%s|%s" % (host, level, filename, line_number, msg, msgFull)
        cs.sendto(MESSAGE, (self._LOG_SERVER_IP, self._LOG_SERVER_PORT))

    def info(self, msg, msgFull=None):
        self._log(self._HOST, self._LOG_LEVEL_INFO, msg, msgFull)

    def warning(self, msg, msgFull=None):
        self._log(self._HOST, self._LOG_LEVEL_WARN, msg, msgFull)

    def fatal(self, msg, msgFull=None):
        self._log(self._HOST, self._LOG_LEVEL_FATAL, msg, msgFull)
