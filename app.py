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

# class Dummy(BaseModel): # Dummy Model
#     # title: string
#     # content: string
    
#     title: str
#     content: str
#     published: bool = True # optional field, default value
#     rating: Optional[int] = None # optional field, default to None

# @app.get("/get_data")
# def get_data():
#     return {"key": "value"}

# @app.post("/post_data")
# # def post_data(payload: dict = Body(...)):
# def post_data(dummy_post_payload: Dummy):
#     # pydantic model -> dict
#     return {"created": dummy_post_payload.dict()}


# CRUD
# Create -> POST /posts
# Read  -> GET /posts
#       -> GET /posts/:id
# Update -> PUT(all field to be sent)/PATCH(only field to be updated to be sent) /posts/:id
# Delete -> DELETE /posts/:id

id_counter = 3
my_posts = [
    {
        "id": 1,
        "title": "My First Post",
        "content": "Excited..."
    },
    {
        "id": 2,
        "title": "Trip to Dubai",
        "content": "Thrilled!"
    }
]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.get("/posts/{id}")
def get_post(id: int):
    return {}

@app.post("/posts")
def save_post(payload: Post):
    global id_counter
    payload_dict = payload.dict()
    payload_dict["id"] = id_counter
    id_counter += 1
    my_posts.append(payload_dict)
    return {"created": payload_dict}
