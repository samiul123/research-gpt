from http.client import BAD_REQUEST, CONFLICT, CREATED, INTERNAL_SERVER_ERROR, NOT_FOUND, OK
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, jsonify, current_app
from app.models import Project, db
from datetime import datetime

from app.schemas import ProjectSchema
from app.exceptions import AppException

projects_bp = Blueprint("projects", __name__)

project_schema = ProjectSchema()

@projects_bp.route("/", methods=["POST"])
def create_project():
    try:
        with db.session.begin():
            project = project_schema.load(data=request.get_json(), session=db.session)
            current_app.logger.debug(f"Creating project: {project_schema.dump(project)}")
            db.session.add(project)
            
        return jsonify(project_schema.dump(project)), CREATED
    
    except ValidationError as e:
        raise AppException(e.messages, status_code=BAD_REQUEST)

    except IntegrityError as e:
        raise AppException("Project already exists", status_code=CONFLICT, payload=str(e))
    
    except Exception as e:
        raise AppException("An error occurred while adding the project", status_code=INTERNAL_SERVER_ERROR, payload=str(e))


@projects_bp.route("/", methods=["GET"])
def get_projects():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    projects = Project.query.paginate(page=page, per_page=per_page, error_out=False)

    result = project_schema.dump(projects.items, many=True)

    return jsonify({
        'total': projects.total,
        'pages': projects.pages,
        'current_page': projects.page,
        'per_page': projects.per_page,
        'has_next': projects.has_next,
        'has_prev': projects.has_prev,
        'projects': result
    })

@projects_bp.route("/<int:project_id>", methods=["GET"])
def get_project(project_id):
    current_app.logger.debug(f"Query project by ID: {project_id}")
    project = Project.query.get(project_id)
    
    if project is None:
        raise AppException("Project not found", status_code=NOT_FOUND)
    
    return jsonify(project_schema.dump(project))
    
@projects_bp.route("/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    try:
        with db.session.begin():
            rows_deleted = db.session.query(Project).filter(Project.id == project_id).delete()
            if rows_deleted == 0:
                raise AppException("Project not found", status_code=NOT_FOUND)
            
        current_app.logger.debug(f"Deleted project with ID: {project_id}")
        return '', OK
    except Exception as e:
        raise AppException("An error occurred while deleting the project", status_code=INTERNAL_SERVER_ERROR, payload=str(e))
    
    
    
    
