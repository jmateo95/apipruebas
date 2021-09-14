from typing import Any, List
from fastapi import APIRouter
from data_connector.elastic.connection import simple_query, simple_nested_query, multiple_agg_query
from pydantic import BaseModel, Json
from typing import Dict, Optional

router = APIRouter()

class simpleYRow(BaseModel):
    value:str
    calculate:str

class YRow(BaseModel):
    name:str
    value:str
    calculate:str

class JsonBodyPie(BaseModel):
    dataset:str
    x:str
    y:simpleYRow
    filters:Optional[Dict]

class JsonBody(BaseModel):
    dataset:str
    type:int
    x:str
    y:List[YRow]
    filters:Optional[Dict]

@router.post("/pie")
async def im_pie(jsonBody : JsonBodyPie):
    return simple_query(jsonBody.dataset, jsonBody.x, jsonBody.y.value, jsonBody.y.calculate)

@router.post("/line_bar")
async def im_line_bar(jsonBody : JsonBody):
    if jsonBody.type==1:
        return simple_nested_query(jsonBody.dataset, jsonBody.x, jsonBody.y[0].name, jsonBody.y[0].value, jsonBody.y[0].calculate)
    else:
        return multiple_agg_query(jsonBody.dataset, jsonBody.x,  jsonBody.y)
