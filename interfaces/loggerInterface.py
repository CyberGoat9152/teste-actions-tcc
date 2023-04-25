from os import environ
from random import random
from datetime import datetime
import requests
import json

async def logger(img, payloadData):
    url = environ.get('LOGGERURI', 'http://logger-api:9122/survey')
    
    payload=json.dumps({
        'request_timestamp':datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f%z"),
        'clientkey':'135e0db4-e2b1-4e48-9ca8-45b4e38e6e2b',
        'user_agent':payloadData['user_agent'],
        'imagespecs':payloadData['imagespecs'],
        'screen':payloadData['screen'],
        'request':payloadData['request'],
        'response':payloadData['response'],
        'ai_inference':payloadData['ai_inference'],
        'backend_inference':payloadData['backend_inference'],
        "route":payloadData['route'],
        "ai_id":"32491fab-80cb-472e-92ca-8289672ce75b",
        'request_token':payloadData['request_token']
    })
    files=[
        ('img',img)
    ]
    headers = {
        'apitoken':'7785a74d-10f1-44f2-ac44-7f51e5a55846',
        'user':payloadData['UUID']
    }
    print(requests.request("POST", url=url, headers=headers, json=payload).status_code)
    print(requests.request("POST", url=url+'/img',headers=headers ,data={'token':payloadData['request_token']},files=files).status_code)
