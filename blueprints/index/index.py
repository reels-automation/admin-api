from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from settings.settings import MODELOS_VOCES

index_router = APIRouter()

@index_router.get("/")
async def personajes():
    return MODELOS_VOCES