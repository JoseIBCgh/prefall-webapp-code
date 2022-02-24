# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from enum import unique

from sqlalchemy import ForeignKeyConstraint

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
    altura = db.Column(db.Float)
    peso = db.Column(db.Float)
    antecedentes_clinicos = db.Column(db.Text)
    centro_id = db.Column(db.Integer, db.ForeignKey('centros.id', ondelete='SET NULL'))
    #tests = db.relationship("Test", backref="paciente", cascade='all, delete-orphan')
    pacientes_asociados = db.relationship(
        "User", secondary='pacientes_asociados',
        primaryjoin=PacienteAsociado.medico_id==id,
        secondaryjoin=PacienteAsociado.paciente_id==id,
        backref='medicos_asociados',
        lazy="dynamic")


class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = 'roles'


class Centro(db.Model):
    __tablename__ = 'centros'
    id = db.Column(db.Integer, primary_key=True)
    cif = db.Column(db.String(20), unique=True)
    nombreFiscal = db.Column(db.String(50))
    direccion = db.Column(db.String(100))
    CP = db.Column(db.Integer)
    ciudad = db.Column(db.String(30))
    provincia = db.Column(db.String(30))
    pais = db.Column(db.String(20))
    usuarios = db.relationship("User", backref="centro")

class Test(db.Model):
    __tablename__ = 'test'
    num_test = db.Column(db.Integer, primary_key = True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    nuevo = db.Column(db.Boolean, unique=False, default=True)
    date = db.Column(db.Date)
    diagnostico = db.Column(db.String(200), nullable=True)

class TestUnit(db.Model):
    __tablename__ = 'test_unit'
    num_test = db.Column(db.Integer)
    id_paciente = db.Column(db.Integer, primary_key=True)
    __table_args__ = (ForeignKeyConstraint([num_test, id_paciente],
                                           [Test.num_test, Test.id_paciente]),
                      {})
    time = db.Column(db.Float(precision=32), primary_key=True)
    acc_x = db.Column(db.Float)
    acc_y = db.Column(db.Float)
    acc_z = db.Column(db.Float)
    gyr_x = db.Column(db.Float)
    gyr_y = db.Column(db.Float)
    gyr_z = db.Column(db.Float)
    mag_x = db.Column(db.Float)
    mag_y = db.Column(db.Float)
    mag_z = db.Column(db.Float)

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

    centro1 = Centro(
        cif="cif1", nombreFiscal="nombre1", direccion="direccion1", CP=1, ciudad="ciudad1",
        provincia="provincia1", pais="pais1")
    centro2 = Centro(
        cif="cif2", nombreFiscal="nombre2", direccion="direccion2", CP=2, ciudad="ciudad2",
        provincia="provincia2", pais="pais2")
    db.session.add_all([centro1, centro2])
    
    if not user_datastore.find_user(username="admin"):
        user_datastore.create_user(
            username="admin", email="admin@kruay.com", 
            password=hash_password("admin"), roles=["admin"]
        )
    
    if not user_datastore.find_user(username="auxiliar"):
        user_datastore.create_user(
            username="auxiliar", email="webapptest2022@gmail.com", centro = centro1,
            password=hash_password("auxiliar"), nombre="auxiliar", roles=["auxiliar"]
        )

    if not user_datastore.find_user(username="auxiliar2"):
        user_datastore.create_user(
            username="auxiliar2", email="auxiliar@kruay.com", centro = centro2,
            password=hash_password("auxiliar2"), nombre="auxiliar2", roles=["auxiliar"]
        )
    
    if not user_datastore.find_user(username="paciente11"):
        user_datastore.create_user(
            username="paciente11", email="paciente11@kruay.com", centro = centro1,
            sexo="V", altura=1.79, peso=97, antecedentes_clinicos="diabetis",
            password=hash_password("paciente11"),nombre="paciente11", roles=["paciente"]
        )
    
    if not user_datastore.find_user(username="paciente12"):
        user_datastore.create_user(
            username="paciente12", email="paciente12@kruay.com", centro = centro1,
            sexo="M", altura=1.56, peso=57, antecedentes_clinicos="cancer de mama",
            password=hash_password("paciente12"), nombre="paciente12", roles=["paciente"]
        )
    
    if not user_datastore.find_user(username="paciente21"):
        user_datastore.create_user(
            username="paciente21", email="paciente21@kruay.com", centro = centro2,
            sexo="V", altura=1.91, peso=75, antecedentes_clinicos="cancer de pulmon, cancer de prostata, problemas hepaticos",
            password=hash_password("paciente21"),nombre="paciente21", roles=["paciente"]
        )
    
    paciente11 = user_datastore.find_user(username="paciente11")
    paciente21 = user_datastore.find_user(username="paciente21")
    if not user_datastore.find_user(username="medico"):
        user_datastore.create_user(
            username="medico", email="medico@kruay.com", centro = centro1,
            password=hash_password("medico"), roles=["medico"], nombre="medico",
            pacientes_asociados=[paciente11, paciente21]
        )
    if not user_datastore.find_user(username="medico1"):
        user_datastore.create_user(
            username="medico1", email="medico1@kruay.com", centro = centro1,
            password=hash_password("medico1"), roles=["medico"], nombre="medico1"
        )  

    if not user_datastore.find_user(username="medico2"):
        user_datastore.create_user(
            username="medico2", email="medico2@kruay.com", centro = centro2,
            password=hash_password("medico2"), roles=["medico"], nombre="medico2"
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

def create_test_data():
    from apps import user_datastore
    user_datastore.find_or_create_role(
        name="auxiliar",
        permissions={"datos-personales-pacientes-centro"},
    )
    if not user_datastore.find_user(username="auxiliar2"):
        user_datastore.create_user(
            username="auxiliar2", email="auxiliar@kruay.com",
            password=hash_password("auxiliar2"), nombre="auxiliar2", roles=["auxiliar"]
        )