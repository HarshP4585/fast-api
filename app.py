from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Schema
# - get all the values from the body
# - data validation
# - force the (client/frontend) to send data in a schema that we expect
# - using "pydantic" -> define schema (can be used with any python code, independent from fastAPI)

class Dummy(BaseModel): # Dummy Model
    # title: string
    # content: string
    
    title: str
    content: str
    published: bool = True # optional field, default value
    rating: Optional[int] = None # optional field, default to None

@app.get("/get_data")
def get_data():
    return {"key": "value"}

@app.post("/post_data")
# def post_data(payload: dict = Body(...)):
def post_data(dummy_post_payload: Dummy):
    # pydantic model -> dict
    return {"created": dummy_post_payload.dict()}
