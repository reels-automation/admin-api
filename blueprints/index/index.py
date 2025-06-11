from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

index_router = APIRouter()

@index_router.get("/")
async def home():
    return "Admin files api"