from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# SQLAlchemy does not allow to update the tables in the database, as SQLAlchemy will look if the table exists in the db, if the table exists then Alchemy will not update the schema
# In such scenarios, Database migration (using Alembic) is the way to go
# Alembic is used to do incremental changes to the db

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_published = Column(Boolean, nullable=False, server_default=text("true"))
    # created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("NOW()"))
    # in production, to update existing table, use databse migration tool like alembic
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # nothing related to DB, but for SQLAlchemy to fetch User's data along with the Post's data
    user = relationship("User")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("NOW()"))

class Vote(Base):
    # intermediate table of posts and users: many to many relationship
    __tablename__ = "votes"

    # composite key: user_id, post_id
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    comment = Column(String, nullable=True)

class RevokedToken(Base):
    __tablename__ = "revoked_token"
    
    token = Column(String, primary_key=True)
