from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, authentication

app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(authentication.router)

# Create Tables from Models
# models.Base.metadata.create_all(bind=engine)

# JWT
# /login {username + password}
# if creds are valid, sign/create a JWT token
# send response back with the token
# all the requests will sent along with the token in the header, /posts {token}
# verify if the token is valid and send the response

# JWT token contains:
# Header(metadata) -> algorithm and token type
# Payload -> any data like id, roles and privilages (but not password/secrets) (anybody can see the token)
# Verify signature -> signature: header + payload + personal secret

# Login process
# /login (username + password(plaintext))
# find user from the username and get hashed password
# verify hased password with the plaintext password by hashing
# if passwords are matched, return token
