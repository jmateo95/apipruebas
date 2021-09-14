from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Request
from data_connector.elastic.connection import simple_query, simple_nested_query, multiple_agg_query
from pydantic import BaseModel, Json
from typing import Dict, Optional
from fastapi import  Request

router = APIRouter()

class prueba(BaseModel):
    shop:str
    token:str
    scope:str

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


class opcional(BaseModel):
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



@router.get("/prueba")
async def hola():
    body={"Respuesta": "hola_desde la API"}
    print('.....')
    print('Hola desde shopify')
    return body


@router.post("/prueba")
async def hola2(prueba : prueba):
    '''
    body={
        "rates": [
            {
                "service_name": "canadapost-overnight",
                "service_code": "ON",
                "total_price": "1295",
                "description": "This is the fastest option by far",
                "currency": "CAD",
                "min_delivery_date": "2013-04-12 14:48:45 -0400",
                "max_delivery_date": "2013-04-12 14:48:45 -0400"
            },
            {
                "service_name": "fedex-2dayground",
                "service_code": "2D",
                "total_price": "2934",
                "currency": "USD",
                "min_delivery_date": "2013-04-12 14:48:45 -0400",
                "max_delivery_date": "2013-04-12 14:48:45 -0400"
            },
            {
                "service_name": "fedex-priorityovernight",
                "service_code": "1D",
                "total_price": "3587",
                "currency": "USD",
                "min_delivery_date": "2013-04-12 14:48:45 -0400",
                "max_delivery_date": "2013-04-12 14:48:45 -0400"
            }
        ]
    }
    '''
    body={'API':'Hola desde la API'}
    print('.....')
    print(prueba)
    return body


@router.post("/rates")
async def hola3(request: Request):
    body={
        "rates": [
            {
                "service_name": "canadapost-overnight",
                "service_code": "ON",
                "total_price": "1295",
                "description": "This is the fastest option by far",
                "currency": "COP",
                "min_delivery_date": "2013-04-12 14:48:45 -0400",
                "max_delivery_date": "2013-04-12 14:48:45 -0400"
            },
            {
                "service_name": "fedex-2dayground",
                "service_code": "2D",
                "total_price": "2934",
                "currency": "COP",
                "min_delivery_date": "2013-04-12 14:48:45 -0400",
                "max_delivery_date": "2013-04-12 14:48:45 -0400"
            },
            {
                "service_name": "fedex-priorityovernight",
                "service_code": "1D",
                "total_price": "3587",
                "currency": "COP",
                "min_delivery_date": "2013-04-12 14:48:45 -0400",
                "max_delivery_date": "2013-04-12 14:48:45 -0400"
            }
        ]
    }
    print('.....')
    print (await request.json())
    return body
