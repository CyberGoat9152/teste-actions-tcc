from os import environ
import requests

async def tempimg(imgbytes, imgname) :
    url = environ.get('SKULLINFOURL','http://info-api:9123/temp-img/upload')
    files = [
        ('img',(f'{imgname}.jpeg', imgbytes ,'image/jpeg'))
    ]
    headers = {}
    response = requests.request("POST", url, headers=headers, files=files)
    return response.text