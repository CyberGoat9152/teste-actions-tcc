from sanic import Blueprint
from sanic.response import json as sanic_json   
from subprocess import check_output

bp_heartbeat = Blueprint('heartbeat')

@bp_heartbeat.get('/', ignore_body=True)
async def beat(request):
    return sanic_json({
        "msg":"ok",
        "time_up":float(check_output(['cat /proc/uptime'],shell=True).decode().split(" ")[0])
    },200)