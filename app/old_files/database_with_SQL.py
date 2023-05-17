import json
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Create connection
# Create cursor
# Execute SQL statements
# Commit connection -> staging changes
# Close cursor
# Close connection

conn = cursor = None

try:
    # host, databse, username, password
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="test",
        cursor_factory=RealDictCursor # ???
    )
    cursor = conn.cursor()
    print("DB connection successfull!!!")
except Exception as e:
    print("DB connection failed...")
    raise e

class Post(BaseModel):
    title: str
    content: str
    is_published: Optional[bool] = True

# limit the output content from the DB
class PostOut(BaseModel):
    id: int
    title: str
    content: str
    is_published: bool
    created_at: str # datetime???

class PostUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    is_published: Optional[bool]

@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id, ))
    post = cursor.fetchone()
    if post:
        return {"data": post}
    return Response(
        status_code=status.HTTP_404_NOT_FOUND,
        content=json.dumps({"data": f"post with id: {id} not found"}),
        media_type="application/json"
    )

@app.post("/posts")
def create_post(payload: Post):
    cursor.execute("""
        INSERT INTO posts (title, content, is_published) VALUES 
        (%s, %s, %s) RETURNING *
    """, (payload.title, payload.content, payload.is_published))
    post = cursor.fetchone()
    conn.commit()
    return Response(
        status_code=status.HTTP_201_CREATED,
        content=json.dumps({"data": post}, default=str),
        media_type="application/json"
    )

@app.patch("/posts/{id}")
def update_post(id: int, payload: PostUpdate):
    query = "UPDATE posts SET "
    key_values = []
    values = []
    for k, v in payload:
        if v:
            key_values.append(" {} = %s".format(k))
            values.append(v)
    query += ",".join(key_values) + " WHERE id = %s RETURNING *"
    values.append(id)
    cursor.execute(query, values)
    post = cursor.fetchone()
    conn.commit()
    if post:
        return {"data": post}
    return Response(
        status_code=status.HTTP_404_NOT_FOUND,
        content=json.dumps({"data": f"post with id: {id} not found"}),
        media_type="application/json"
    )

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id, ))
    post = cursor.fetchone()
    conn.commit()
    if post:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(
        status_code=status.HTTP_404_NOT_FOUND,
        content=json.dumps({"data": f"post with id: {id} not found"}),
        media_type="application/json"
    )
