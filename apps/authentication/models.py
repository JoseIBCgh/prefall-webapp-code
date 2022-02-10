# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from enum import unique

from apps import db

from flask_security import hash_password

from flask_security.models import fsqla_v2 as fsqla

fsqla.FsModels.set_db_info(db, user_table_name="users", role_table_name="roles")

class User(db.Model, fsqla.FsUserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    nombre = db.Column(db.String(50))
    fecha_nacimiento = db.Column(db.Date)
    sexo = db.Column(db.String(1))
    altura = db.Column(db.Numeric)
    peso = db.Column(db.Numeric)
    antecedentes_clinicos = db.Column(db.Text)


class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = 'roles'

'''
@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
'''

def create_users():
    from apps import user_datastore
    user_datastore.find_or_create_role(
        name="admin",
        permissions={"datos-personales-pacientes-centro", "datos-personales-personal-centro"},
    )
    user_datastore.find_or_create_role(
        name="medico",
        permissions={"datos-personales-pacientes-asociados", "datos-clinicos-pacientes-asociados"},
    )
    user_datastore.find_or_create_role(
        name="auxiliar",
        permissions={"datos-personales-pacientes-centro"},
    )
    user_datastore.find_or_create_role(
        name="paciente",
        permissions={},
    )

    if not user_datastore.find_user(username="admin"):
        user_datastore.create_user(
            username="admin", email="admin@kruay.com", 
            password=hash_password("admin"), roles=["admin"]
        )
    
    if not user_datastore.find_user(username="medico"):
        user_datastore.create_user(
            username="medico", email="medico@kruay.com", 
            password=hash_password("medico"), roles=["medico"]
        )
    
    if not user_datastore.find_user(username="auxiliar"):
        user_datastore.create_user(
            username="auxiliar", email="webapptest2022@gmail.com",
            password=hash_password("auxiliar"), roles=["auxiliar"]
        )

    db.session.commit()