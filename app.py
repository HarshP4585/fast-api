from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/get_data")
def get_data():
    return {"key": "value"}

@app.post("/post_data")
def post_data(payload: dict = Body(...)):
    return {"created": payload}
