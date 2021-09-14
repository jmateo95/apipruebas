from fastapi import FastAPI
from fastapi import Request

app = FastAPI()

#domain where this api is hosted for example : localhost:5000/docs to see swagger documentation automagically generated.


@app.get("/")
def home():
    return {"message":"Hello TutLinks.com"}

@app.post("/rates")
async def hola(request: Request):
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