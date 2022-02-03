# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from enum import unique
from flask_login import UserMixin, AnonymousUserMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, username, password, role):
        self.username = username
        self.password = hash_pass(password)
        self.role = Role.query.filter_by(name=role).first()
    '''
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)
    '''
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    @staticmethod
    def insert_users():
        users = [
            {"username": "medico", "password": "medico", "role" : "Medico" },
            {"username": "auxiliar", "password": "auxiliar", "role" : "Auxiliar" },
            {"username": "paciente", "password": "paciente", "role" : "Paciente" },
            {"username": "admin", "password": "admin", "role" : "Admin" }
        ]
        for u in users:
            user = Users.query.filter_by(username=u["username"]).first()
            if user is None:
                user = Users(u["username"], u["password"], u["role"])
            db.session.add(user)
        db.session.commit()

    def __repr__(self):
        return str(self.username)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

class Permission:
    DATOS_PERSONALES_PACIENTES_ASOCIADOS = 1
    DATOS_PERSONALES_PACIENTES_CENTRO = 2
    DATOS_CLINICOS_PACIENTES_ASOCIADOS = 4
    ADMIN = 8

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('Users', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm
    
    @staticmethod
    def insert_roles():
        roles = {
            'Medico': [Permission.DATOS_CLINICOS_PACIENTES_ASOCIADOS,
            Permission.DATOS_PERSONALES_PACIENTES_ASOCIADOS],
            'Auxiliar': [Permission.DATOS_PERSONALES_PACIENTES_CENTRO],
            'Paciente': [],
            'Admin': [Permission.ADMIN]
        }
        default_role = 'Paciente'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None

login_manager.anonymous_user = AnonymousUser