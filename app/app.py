from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import accounts, posts, users, votes

app = FastAPI()

origins = [ # strict access to API
    "https://www.google.com",
    "https://www.youtube.com"
]

app.add_middleware( # a function that runs before every request
    CORSMiddleware,
    allow_origins=origins, # ["*"] -> public API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(votes.router)

# Create Tables from Models
# models.Base.metadata.create_all(bind=engine)


# TODO -----
# Using sessions
# Relationships 1-1, 1-many, ...
# Join columns in SQLAlchemy
# Transactions in DB
# Async
# Create Microservices
# -----


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

# Verification process
# Create function for verifying access token by decoding the JWT and return user if the token is valid + not expired
# add a variable dependency of (get user function) in the controller definition
# if the user variable is valid, then continue the operation else, raise auth error

# how to deal with null values for FK in existing table data?

# Alembic setup
# alembic init
# import Alchemy Base (from the models file as it alembic will have access to read models as well) class in the env.py file and update target_metadata
# update sqlalchemy.url in the alembic.ini file with the database url
#   Not recommended because of security reasons
#   Hence, override "sqlalchemy.url" in the env.py and use "set_main_option" of the config and set the database url with env variables
# alembic revision -m "descriptive message for migration"
#   This will create a revision python file where upgrade and downgrade steps are to be mentioned
# reflect migration to the db -> alembic upgrade revision_id
# use --autogenerate flag to sync changes between DB and SQLAlchemy models

# Getting data in the browser from API call:
# fetch("http://localhost:8000/posts").then(resp => resp.json()).then(console.log)
# - Promise {<pending>}
# - Access to fetch at 'http://localhost:8000/posts' from origin 'https://www.google.com' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource. If an opaque response serves your needs, set the request's mode to 'no-cors' to fetch the resource with CORS disabled.
# blocked by CORS (Cross Origin Resource Sharing) policy
# the origin of request is mentioned in the request header
# cors allow to make request from web browser on one domain to a server on different domain
# by default our API will only allow web browsers running on the same domain to make request to it
# add cors middleware to the app

# **************************************
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=40468s
# https://www.youtube.com/watch?v=IZUjJ3rPY1E
# https://www.youtube.com/watch?v=Cy9fAvsXGZA
# **************************************

# DEPLOYMENT

# 1. Heroku

# install heroku cli
# heroku create <app-name>
#   To create an app, verify your account by adding payment information. Verify now at https://heroku.com/verify
# git remote -> list remote destinations of the repo
# git push heroku main -> push code to heroku and create instance of the app

# how to run the app?
# create a file Procfile for command to start application
# web: uvicorn app.app:app --host=0.0.0.0 --port=${PORT:-5000}
# push the changes to the git again with the Procfile

# add postgres db on heroku
# https://devcenter.heroku.com/articles/heroku-postgresql
# heroku addons:create heroku-postgresql:<PLAN-NAME=hobby-dev>
# save db creds from heroku like: url, username, password, etc.
# create config vars ie. env vars for heroku as per the code
# restart app -> heroku ps:restart
# app info -> heroku apps:info <APP-NAME>

# create alembic migrations for creating prod databases like dev env
# upgrade the alembic revisions by runnning command:
#   heroku run "alembic upgrade head"

# pushing changes to heroku: "git push heroku main" (after adding, commiting and pushing onto git)

# 2. Ubuntu Server

# Using NGINX as proxy webserver (gateway)
# Can handle SSL termination

# HTTPS -> NGINX -> HTTP -> SERVICE
