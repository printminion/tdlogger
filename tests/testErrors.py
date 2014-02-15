import sys
import traceback

__author__ = 'cr'

from tdlogger import tdlogger
import settings

logger = tdlogger('host1', settings.LOG_SERVER_IP, settings.LOG_SERVER_PORT)
#put session data here
logger.session = {'session_id': 'cda84c2176977ee3b012b49f1cec2511', 'remote_host': '<REMOTE_HOST>'}

logger.info('hallo world')
logger.warning('hallo world', {'user_id': 1111111, 'headers': ['Content-Type: application/json'], 'otherdata': 'yey!'})

try:
   run_my_stuff()
except:
    logger.exception('Got exception on main handler', {'traceback': traceback.format_exc()})
    pass


