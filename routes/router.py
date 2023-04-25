from .heartbeat.heartbeat import bp_heartbeat
from .check_url.check_url import bp_check_url
from .check.check import bp_check

def router(app):
    app.blueprint(bp_heartbeat)
    app.blueprint(bp_check_url)
    app.blueprint(bp_check)