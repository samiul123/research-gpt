from os import name
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.models import Project


class ProjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        load_instance = True
        sqla_session = None
    
    id = auto_field()
    name = auto_field()
    creation_date = auto_field()