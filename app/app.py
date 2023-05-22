from fastapi import FastAPI
from . import models
from .database import engine
from .routers import accounts, posts, users, votes

app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(votes.router)

# Create Tables from Models
# models.Base.metadata.create_all(bind=engine)


# TODO -----
# Relationships 1-1, 1-many, ...
# Join columns in SQLAlchemy
# Transactions in DB
# Async
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
