from functools import wraps
from flask import abort, url_for, redirect, request
from flask_security import current_user

from apps.authentication.models import Centro, User

def admin_centro_access():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if current_user.has_role('admin'):
                return f(*args, **kwargs)
            if not current_user.has_role('admin-centro'):
                abort(403)
            id = request.view_args["id_centro"]
            centro = Centro.query.filter_by(id=id).first()
            if centro.id_admin != current_user.id:
                abort(403)
            else:
                return f(*args, **kwargs)
        return wrapper
    return decorator

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
                if paciente.id_centro == current_user.id_centro:
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

def patient_data_access():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.has_role('paciente'):
                abort(403)
            id = request.view_args["id"]
            if int(id) != current_user.id:
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator