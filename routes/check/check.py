from sanic import Blueprint
from sanic.response import json as sanic_json
from os import environ

from io import BytesIO
from PIL import Image
import time

from apiutils.auth import protected
from apiutils.tokenGenerator import getToken

from interfaces.kpaInterface import KPAia_model
from interfaces.tempimgInterface import tempimg
from interfaces.loggerInterface import logger


bp_check = Blueprint('check')

@bp_check.post('/check')
@protected
async def Check(request):
    back_inference = time.time()
    devEnv = environ.get('ISADEVENV', 'True') == 'True'
    try:
        # Variable
        response = {}
        valid_files = ['jpg','jpeg','png']
        # Get image on request
        image_form_data = request.files.get('img')
        extension = str(image_form_data.type).split('/')[-1].lower()
        userID = request.form.get('user')
    
        if str(extension) in valid_files:
            # convert image to correct format
            req = {}
            req['user'] = request.form.get('user')
            req['apitoken'] = request.form.get('apitoken')
            img = Image.open(BytesIO(image_form_data.body))
                        
            # Get request token
            token = await getToken()
            # process the image using YOLO5
            ai_inference = time.time()
            KPAia_model.predict(img)
            ai_inference = time.time() - ai_inference
            
            response['payload'] = KPAia_model.digest2JSON()
            resp = {'msg':'ok','reqToken': token, 'retorno_ia':response['payload']}
                        # Save processed image to info-apis
            if environ.get("REGISTERPROCESSIMAGE") == 'True':
                try:
                    await tempimg(KPAia_model.digest2Image(), token)
                except Exception:
                    pass
            # Save current request in logger
            if environ.get("REGISTERTOLOGGER") == 'True':
                try:
                    await logger(img=image_form_data , payloadData={
                        "request_token":token,
                        "user_agent":request.headers.get("user-agent"),
                        "imagespecs":{
                            "size":img.size,
                            "widht":img.width,
                            "heigth":img.height,
                            "bits":-1,
                            "mode":img.mode,
                            "info":{"not_implemented":"not_implemented"},
                            "layers":-1
                            },
                        "screen":"unknown",
                        "request": req,
                        "response": resp,
                        "ai_inference":ai_inference,
                        "route":"/check",
                        "backend_inference":f'{time.time() - back_inference}',
                        "UUID":userID}
                    )
                except Exception:
                    pass
            return sanic_json(resp, 200)

            
        else:
            # If is a not valid format
            response['Status'] = "Error" 
            response['Message'] = "Wrong image format jpg, jpeg ou png."
            return sanic_json(response, 400)
        
    except Exception as e:
        response = {}
        code = 0
        if "'NoneType' object has no attribute 'type'" in f'{e}':
            # Are missing image in request
            code = 400
            response['Status'] = "Error"
            response['Message'] = "Missing image file, the parameter is 'img' and must be sent by form-data, see more in https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST"
        else:
            # Don't send error to response, it's a security vunerability
            code = 500
            response['Status'] = "Error"
            response['Message'] = 'Internal server error'
            if devEnv:
                response['error'] = str(e)
                print(e)
        return sanic_json(response, code)
