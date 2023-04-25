from functools import wraps

from sanic import json as sacni_json
import json


def check_token(request):
    
    mock_api_token = "32491fab-80cb-472e-92ca-8289672ce75b"
    mock_users = [
        'c7c03de7-fdb4-4551-9e6a-2a7abedb52a0',
        '0a7016a0-fbae-4175-ab85-e9c02259cb6e',
        '9839827f-6ae7-494c-9361-8b1f0031204b',
        '67369147-5f12-4c10-941d-827a7056682d',
        'f1a084bc-0b4f-4f36-b523-f2527c8cd84c'
    ]
    
    if b'auth' in request.body and request.files == {}:
        data = json.loads(request.body.decode())['auth']
    else:
        data = {
        'apitoken':request.form.get('apitoken'),
        'user': request.form.get('user')
        }
    if data['apitoken'] == mock_api_token and data['user'] in mock_users:
        return True
    else:
        return False

def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = check_token(request)

            if is_authenticated:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return sacni_json({"msg":"You are unauthorized."}, status=401)

        return decorated_function

    return decorator(wrapped)