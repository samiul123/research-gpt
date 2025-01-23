from app import db
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy.inspection import inspect
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Project(db.Model):
    __tablename__ = "projects"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    

# class Chat(db.Model):
#     __tablename__ = "chats"

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255), nullable=False)
#     creation_date = db.Column(db.DateTime, default=datetime.utcnow)
#     project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

# class Message(db.Model):
#     __tablename__ = "messages"

#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.Text, nullable=False)
#     creation_date = db.Column(db.DateTime, default=datetime.utcnow)
#     chat_id = db.Column(db.Integer, db.ForeignKey("chats.id"), nullable=False)
