from functools import wraps
from flask import abort, url_for, redirect, request
from flask_security import current_user

from apps.authentication.models import User

def personal_data_access():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if current_user.has_role('admin'):
                return f(*args, **kwargs)
            if current_user.has_role('auxiliar'):
                id = request.view_args["id"]
                paciente = User.query.filter_by(id=id).first()
                if paciente is None:
                    abort(404)
                if not paciente.has_role('paciente'):
                    abort(403)
                if paciente.centro_id == current_user.centro_id:
                    return f(*args, **kwargs)
            abort(403)
        return wrapper
    return decorator

def clinical_data_access():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.has_role('medico'):
                abort(403)
            id = request.view_args["id"]
            paciente = User.query.filter_by(id=id).first()
            if paciente is None:
                abort(404)
            if not paciente.has_role('paciente'):
                abort(403)
            pacientes_medico = current_user.pacientes_asociados
            if not paciente in pacientes_medico:
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator