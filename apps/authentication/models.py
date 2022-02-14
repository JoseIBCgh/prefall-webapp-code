# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from enum import unique

from apps import db

from flask_security import hash_password

from flask_security.models import fsqla_v2 as fsqla

fsqla.FsModels.set_db_info(db, user_table_name="users", role_table_name="roles")

class PacienteAsociado(db.Model):
    __tablename__ = 'pacientes_asociados'
    paciente_id = db.Column(db.Integer,db.ForeignKey('users.id'), primary_key=True)
    medico_id = db.Column(db.Integer,db.ForeignKey('users.id'), primary_key=True)

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
    centro_id = db.Column(db.Integer, db.ForeignKey('centros.id'))
    pacientes_asociados = db.relationship(
        "User", secondary='pacientes_asociados',
        primaryjoin=PacienteAsociado.medico_id==id,
        secondaryjoin=PacienteAsociado.paciente_id==id,
        backref='medicos_asociados')


class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = 'roles'


class Centro(db.Model):
    __tablename__ = 'centros'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    usuarios = db.relationship("User", backref="centro")

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

def create_data():
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

    centro1 = Centro(id = 1, nombre="nombre1")
    centro2 = Centro(id = 2, nombre="nombre2")
    db.session.add_all([centro1, centro2])

    if not user_datastore.find_user(username="admin"):
        user_datastore.create_user(
            username="admin", email="admin@kruay.com", 
            password=hash_password("admin"), roles=["admin"]
        )
    
    if not user_datastore.find_user(username="auxiliar"):
        user_datastore.create_user(
            username="auxiliar", email="webapptest2022@gmail.com", centro = centro1,
            password=hash_password("auxiliar"), roles=["auxiliar"]
        )

    if not user_datastore.find_user(username="auxiliar2"):
        user_datastore.create_user(
            username="auxiliar2", email="auxiliar@kruay.com", centro = centro2,
            password=hash_password("auxiliar2"), roles=["auxiliar"]
        )
    
    if not user_datastore.find_user(username="paciente11"):
        user_datastore.create_user(
            username="paciente11", email="paciente11@kruay.com", centro = centro1,
            password=hash_password("paciente11"),nombre="paciente11", roles=["paciente"]
        )
    
    if not user_datastore.find_user(username="paciente12"):
        user_datastore.create_user(
            username="paciente12", email="paciente12@kruay.com", centro = centro1,
            password=hash_password("paciente12"), nombre="paciente12", roles=["paciente"]
        )
    
    if not user_datastore.find_user(username="paciente21"):
        user_datastore.create_user(
            username="paciente21", email="paciente21@kruay.com", centro = centro2,
            password=hash_password("paciente21"),nombre="paciente21", roles=["paciente"]
        )
    
    paciente11 = user_datastore.find_user(username="paciente11")
    paciente21 = user_datastore.find_user(username="paciente21")

    if not user_datastore.find_user(username="medico"):
        user_datastore.create_user(
            username="medico", email="medico@kruay.com", centro = centro1,
            password=hash_password("medico"), roles=["medico"], 
            pacientes_asociados=[paciente11, paciente21]
        )
    
    db.session.commit()

def asociar_pacientes():
    from apps import user_datastore
    medico = user_datastore.find_user(username="medico")
    paciente11 = user_datastore.find_user(username="paciente11")
    paciente21 = user_datastore.find_user(username="paciente21")

    medico.pacientes_asociados.append(paciente11)
    medico.pacientes_asociados.append(paciente21)

    db.session.add(medico)

    db.session.commit()