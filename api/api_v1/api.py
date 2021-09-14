from fastapi import APIRouter

from api.api_v1.endpoints import charts

api_router = APIRouter()
api_router.include_router(charts.router, prefix="/charts", tags=["charts"])