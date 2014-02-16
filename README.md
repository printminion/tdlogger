tdlogger
========

# Install requirements
```shell
pip install -r requirements.txt
```
#start daemon
```shell
ndlogger-daemon.py
```


Usage
======
```python
import traceback
import settings
from tdlogger import tdlogger

#initialize logger
logger = tdlogger('host1', settings.LOG_SERVER_IP, settings.LOG_SERVER_PORT)

#adding session data here
logger.session = {'session_id': 'cda84c2176977ee3b012b49f1cec2511', 'remote_host': '<REMOTE_HOST>'}

#logging info message
logger.info('hallo world')

#logging warniing with custom data
logger.warning('hallo world', {'user_id': 1111111, 'headers': ['Content-Type: application/json'], 'otherdata': 'yey!'})

#logging exception with traceback
try:
   run_my_stuff()
except:
    logger.exception('Got exception on main handler', {'traceback': traceback.format_exc()})
    pass
```

API
===
GET /api/messages/?format=json
------------------------------
```javascript
[
    {
        "id": "52ff8b260daae019b20c2283",
        "timestamp": "2014-02-15T16:43:34.439",
        "level": "exception",
        "source": "host2",
        "message": "Got exception on main handler"
    },
    {
        "id": "52ff8b260daae019b20c2281",
        "timestamp": "2014-02-15T16:43:34.438",
        "level": "info",
        "source": "host2",
        "message": "hallo world"
    }
]
```

GET /api/messages/{messageId}/?format=json
------------------------------------------
Example #1
```python
logger.exception('Got exception on main handler', {'traceback': traceback.format_exc()})
```
```javascript
[
    {
        "id": "52ff83df0daae019b20c227d",
        "timestamp": "2014-02-15T16:12:31.849",
        "level": "exception",
        "source": "host1",
        "message": "Got exception on main handler",
        "filename": "/home/cr/develop/python/tdlogger/tests/testErrors.py",
        "line_number": 19,
        "session": {
            "traceback": "Traceback (most recent call last):\n  File \"/home/cr/develop/python/tdlogger/tests/testErrors.py\", line 17, in <module>\n    run_my_stuff()\nNameError: name 'run_my_stuff' is not defined\n"
        },
        "payload": {
            "remote_host": "<REMOTE_HOST>"
        }
    }
]
```
Example #2
```python
logger.warning('hallo world', {'user_id': 1111111, 'headers': ['Content-Type: application/json'], 'otherdata': 'yey!'})
```
```javascript
[
    {
        "id": "52ff8b260daae019b20c2282",
        "timestamp": "2014-02-15T16:43:34.438",
        "level": "warning",
        "source": "host2",
        "message": "hallo world",
        "filename": "/home/cr/develop/python/tdlogger/tests/testErrors.py",
        "line_number": 14,
        "session": {
            "headers": [
                "Content-Type: application/json"
            ],
            "user_id": 1111111,
            "otherdata": "yey!"
        },
        "payload": {
            "remote_host": "<REMOTE_HOST>"
        }
    }
]

]
```
POST /api/messages/getnewmessagecount/?format=json
--------------------------------------------------
Request:
```javascript
{"since": 1392571166006}
```
Response:
```javascript
{
    "ok": "true",
    "payload": 334
}
```

TODO
====
* get messages by host
* get messages by session
* get messages by user_id