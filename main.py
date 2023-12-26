import uvicorn
from fastapi import FastAPI
from api import task_api
from views import home
from starlette.staticfiles import StaticFiles

api = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})


def config_routing():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(task_api.router)
    api.include_router(home.router)


if __name__ == '__main__':
    config_routing()
    uvicorn.run('main:api', host='127.0.0.1', port=8000)
else:
    config_routing()
