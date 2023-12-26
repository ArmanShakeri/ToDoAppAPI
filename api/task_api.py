from typing import List

from fastapi import APIRouter, Response
from utils.logger import Logger
from models.task import Task, UpdatedTask
from models import responses
import json
from connections.aioredis_db import RedisDB

logger = Logger()
router = APIRouter()
instance = RedisDB().redis_connection


@router.get('/task', response_model=List[Task])
async def get_all_tasks():
    try:
        keys = await instance.keys()
        data = await instance.mget(keys)
        results = []
        for item in data:
            results.append(json.loads(item))
        results = json.dumps(results)
        return Response(content=results, media_type="application/json")
    except Exception as e:
        logger.error(e.__str__())
        return Response(status_code=500, content='{"detail": "Internal Server Error"}', media_type="application/json")


@router.get('/tasks/{task_id}')
async def get_task(task_id: int):
    try:
        if not await instance.exists(task_id):
            msg = {"detail": f"Task {task_id} not found"}
            return Response(status_code=404, content=json.dumps(msg), media_type="application/json")
        else:
            value = json.loads(await instance.get(task_id))
            return value

    except Exception as e:
        logger.error(e.__str__())
        return Response(status_code=500, content='{"detail": "Internal Server Error"}', media_type="application/json")


@router.post('/tasks', response_model=responses.Response)
async def create_task(task: Task):
    try:
        if await instance.exists(task.id):
            msg = {"detail": f"Task {task.id} already exists"}
            return Response(status_code=404, content=json.dumps(msg), media_type="application/json")
        else:
            await instance.set(task.id, task.model_dump_json())
            msg = {"detail": f"Task {task.id} successfully created"}
            return Response(status_code=201, content=json.dumps(msg), media_type="application/json")
    except Exception as e:
        logger.error(e.__str__())
        return Response(status_code=500, content='{"detail": "Internal Server Error"}', media_type="application/json")


@router.put('/tasks/{task_id}', response_model=responses.Response)
async def update_task(task_id: int, task: UpdatedTask):
    try:
        if not await instance.exists(task_id):
            msg = {"detail": "Task not found"}
            return Response(status_code=404, content=json.dumps(msg), media_type="application/json")

        if task.id is None or task.id == task_id:
            msg = {"detail": f"Task {task.id} successfully updated"}
        else:
            task.id = task_id
            msg = {"detail": f"Task {task.id} successfully updated. 'id' in the json file not equal to task_id,so it replaced with the task_id"}

        await instance.set(task_id, task.model_dump_json())
        return Response(status_code=200, content=json.dumps(msg), media_type="application/json")

    except Exception as e:
        logger.error(e.__str__())
        return Response(status_code=500, content='{"detail": "Internal Server Error"}', media_type="application/json")


@router.delete('/tasks/{task_id}', response_model=responses.Response)
async def delete_task(task_id: int):
    try:
        if not await instance.exists(task_id):
            msg = {"detail": f"Task {task_id} not found"}
            return Response(status_code=404, content=json.dumps(msg), media_type="application/json")
        else:
            await instance.delete(task_id)
            msg = {"detail": f"Task {task_id} successfully deleted"}
            return Response(status_code=200, content=json.dumps(msg), media_type="application/json")

    except Exception as e:
        logger.error(e.__str__())
        return Response(status_code=500, content='{"detail": "Internal Server Error"}', media_type="application/json")
