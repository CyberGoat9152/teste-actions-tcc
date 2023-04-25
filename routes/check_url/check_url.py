from sanic import Blueprint
from sanic.response import json as sanic_json

from io import BytesIO
from PIL import Image

from apiutils.auth import protected
from apiutils.tokenGenerator import getToken

from interfaces.kpaInterface import KPAia_model
from interfaces.loggerInterface import logger
from interfaces.tempimgInterface import tempimg

import requests
from os import path, remove, environ
import time

bp_check_url = Blueprint('check-url')

@bp_check_url.post('/check-url')
@protected
async def checkUrl(request):
    back_inference = time.time()
    devEnv = environ.get('ISADEVENV', 'False') == 'True'
    try:
        # Variable
        response = {}
        req = {}
        # Get image on request
        if request.headers.get('Content-Type') == 'application/json':
            req = dict(request.json)
            uri = req['url']
        else:
            uri = request.form.get('url')
            req['url'] = request.form.get('url')
            req['user'] = request.form.get('user')
            req['apitoken'] = request.form.get('apitoken')
        
        image_from_url = requests.get(uri).content
        img = Image.open(BytesIO(image_from_url))
        img = img.convert('RGB')

        token = await getToken()   
        # Conver to image file
        img.save(f'{token}.jpeg')
        img = Image.open(f'{token}.jpeg')

        if 'apitoken' in req:
            userID = req['user']

        else:
            userID = req['auth']['user']

        # Process the image using YOLO5
        ai_inference = time.time()
        KPAia_model.predict(img)
        ai_inference = time.time() - ai_inference
        
        # If the services is offline just continue
        try:
            # Save processed image to info-apis
            if environ.get("REGISTERPROCESSIMAGE") == 'True':
                await tempimg(KPAia_model.digest2Image(), token)
            # Save current request in logger
            if environ.get("REGISTERTOLOGGER") == 'True':
                await logger(image_from_url, token=token, UUID=userID)
        except:
            pass
        response['payload'] = KPAia_model.digest2JSON()

        resp = {'msg':'ok','reqToken': token, 'retorno_ia':response['payload']}
        
        # Cache clear
        if path.exists(f'{token}.jpeg'):
            remove(f'{token}.jpeg')
        if path.exists(f'/code/{token}.jpeg'):
            remove(f'/code/{token}.jpeg')
        
        # Save processed image to info-apis
        if environ.get("REGISTERPROCESSIMAGE") == 'True':
            try:
                await tempimg(KPAia_model.digest2Image(), token)
            except Exception:
                pass
        # Save current request in logger
        if environ.get("REGISTERTOLOGGER") == 'True':
            try:
                await logger(image_from_url, payloadData={
                    "request_token":token,
                    "user_agent":request.headers.get("user-agent"),
                    "imagespecs":{
                        "size":img.size,
                        "widht":img.width,
                        "heigth":img.height,
                        "bits":img.bits,
                        "mode":img.mode,
                        "info":img.info,
                        "layers":img.layers
                        },
                    "screen":"unknown",
                    "request": req,
                    "response": resp,
                    "ai_inference":ai_inference,
                    "backend_inference":f'{time.time() - back_inference}',
                    "route":"/check-url",
                    "UUID":userID}
                )
            except Exception as e:
                print(e)
                pass
        del img, userID, uri
        return sanic_json(resp, 200)
            
    except Exception as e:
        response = {}
        code = 0
        if "'NoneType' object has no attribute 'type'" in f'{e}' or "None" in f'{e}' or 'url' in f'{e}':
            # Are missing image in request
            code = 400
            response['Status'] = "Error"
            response['Message'] = "Missing image file, the parameter is 'url' and must be sent by form-data or by body in json, see more in https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST"
        else:
            # Don't send error to response, it's a security vunerability
            code = 500
            response['Status'] = "Error"
            response['Message'] = 'Internal server error'
            if devEnv:
                response['Message'] = str(e)
                print(e)
        return sanic_json(response, code)