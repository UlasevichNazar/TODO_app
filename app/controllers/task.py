from logging import getLogger

from fastapi import APIRouter

logger = getLogger(__name__)

task_router = APIRouter(prefix="/task", tags=["task"])
