from sanic import Sanic
from routes.router import router
import os

env_host = os.environ.get('HOST', '0.0.0.0')
env_port = int(os.environ.get('PORT', 8080))
env_workers = int(os.environ.get('WORKERS', 1))
env_debug = True if os.environ.get('DEBUG', 'True') == 'True' else False
env_fast_flag = True if os.environ.get('FAST', 'True') == 'True' else False
env_auto_reload = True if os.environ.get('AUTORELOAD', 'True') == 'True' else False

app = Sanic('skull')
router(app)

if __name__ == "__main__":
    if env_fast_flag:
        app.run(
            host=env_host,
            port=env_port,
            debug=env_debug,
            auto_reload=env_auto_reload,
            workers=env_workers
    )
    else:
        app.run(
            host=env_host,
            port=env_port,
            debug=env_debug,
            auto_reload=env_auto_reload,
            fast=env_fast_flag
    )
