__author__ = 'cr'

from tdlogger import tdlogger
import settings

logger = tdlogger('host1', settings.LOG_SERVER_IP, settings.LOG_SERVER_PORT)


logger.info('hallo world', 'info message')
logger.warning('hallo world', 'warning message')
logger.fatal('hallo world', 'fatal message')
