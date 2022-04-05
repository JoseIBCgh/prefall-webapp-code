# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from enum import unique

from sqlalchemy import ForeignKeyConstraint, event

from apps import db

from flask_security import hash_password

from flask_security.models import fsqla_v2 as fsqla

fsqla.FsModels.set_db_info(db, user_table_name="users", role_table_name="roles")

class PacienteAsociado(db.Model):
    __tablename__ = 'pacientes_asociados'
    id_paciente = db.Column(db.Integer,db.ForeignKey('users.id'), primary_key=True)
    id_medico = db.Column(db.Integer,db.ForeignKey('users.id'), primary_key=True)

class User(db.Model, fsqla.FsUserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    identificador = db.Column(db.String(10), unique=True)
    username = db.Column(db.String(20), unique=True)
    nombre = db.Column(db.String(50))
    fecha_nacimiento = db.Column(db.Date)
    sexo = db.Column(db.String(1))
    altura = db.Column(db.Float)
    peso = db.Column(db.Float)
    antecedentes_clinicos = db.Column(db.Text)
    id_centro = db.Column(db.Integer, db.ForeignKey('centros.id', ondelete='SET NULL'))
    tests = db.relationship("Test", backref="paciente", cascade='all, delete-orphan')
    pacientes_asociados = db.relationship(
        "User", secondary='pacientes_asociados',
        primaryjoin=PacienteAsociado.id_medico==id,
        secondaryjoin=PacienteAsociado.id_paciente==id,
        backref='medicos_asociados',
        lazy="dynamic")
    tests_de_pacientes = db.relationship("AccionesTestMedico", backref="medico", lazy="dynamic", cascade='all, delete-orphan')


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
    usuarios = db.relationship("User", backref="centro", foreign_keys=[User.id_centro])
    tests = db.relationship("Test", backref="centro", lazy="dynamic")
    id_admin = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL', 
    use_alter=True, name='fk_id_admin'))

class Test(db.Model):
    __tablename__ = 'test'
    num_test = db.Column(db.Integer, primary_key = True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    id_centro = db.Column(db.Integer, db.ForeignKey('centros.id', ondelete='SET NULL'))
    date = db.Column(db.Date)
    bow = db.Column(db.Float, nullable=True)
    fall_to_left = db.Column(db.Float, nullable=True)
    fall_to_right = db.Column(db.Float, nullable=True)
    falling_backward = db.Column(db.Float, nullable=True)
    falling_forward = db.Column(db.Float, nullable=True)
    idle = db.Column(db.Float, nullable=True)
    sitting = db.Column(db.Float, nullable=True)
    sleep = db.Column(db.Float, nullable=True)
    standing = db.Column(db.Float, nullable=True)
    model = db.Column(db.Integer, db.ForeignKey('model.id'), nullable=True)

class GraphJson(db.Model):
    __tablename__ = 'graph_json'
    num_test = db.Column(db.Integer, primary_key = True)
    id_paciente = db.Column(db.Integer, primary_key=True)
    __table_args__ = (ForeignKeyConstraint([num_test, id_paciente],
                                           [Test.num_test, Test.id_paciente]),
                      {})
    graph = db.Column(db.JSON)

class Model(db.Model):
    __tablename__ = 'model'
    id = db.Column(db.Integer, primary_key=True)
    boundaries = db.relationship("Boundary", backref="model", lazy="dynamic", cascade='all, delete-orphan')
    training_points = db.relationship("TrainingPoint", backref="model", lazy="dynamic", cascade='all, delete-orphan')

class Boundary(db.Model):
    __tablename__ = 'boundary'
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'), primary_key=True)
    index = db.Column(db.Integer, primary_key = True)
    intercept = db.Column(db.Float)
    coef0 = db.Column(db.Float)
    coef1 = db.Column(db.Float)
    coef2 = db.Column(db.Float)

class TrainingPoint(db.Model):
    __tablename__ = 'training_point'
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'), primary_key=True)
    index = db.Column(db.Integer, primary_key = True)
    clase = db.Column(db.String(20))
    acc_x = db.Column(db.Float)
    acc_y = db.Column(db.Float)
    acc_z = db.Column(db.Float)

class TestUnit(db.Model):
    __tablename__ = 'test_unit'
    num_test = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, primary_key=True)
    __table_args__ = (ForeignKeyConstraint([num_test, id_paciente],
                                           [Test.num_test, Test.id_paciente]),
                      {})
    item = db.Column(db.Integer)
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

class AccionesTestMedico(db.Model):
    __tablename__ = "acciones_test_medico"
    num_test = db.Column(db.Integer, primary_key = True)
    id_paciente = db.Column(db.Integer, primary_key=True)
    __table_args__ = (ForeignKeyConstraint([num_test, id_paciente],
                                           [Test.num_test, Test.id_paciente]),
                      {})
    id_medico = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    visto = db.Column(db.Boolean, default = False, nullable=False)
    diagnostico = db.Column(db.Text, nullable=True)

class DocumentoPaciente(db.Model):
    __tablename__ = "documentos_paciente"
    id_paciente = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    id_medico = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    id_file = db.Column(db.Integer, db.ForeignKey('files.id'), primary_key=True)

class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

'''
import sys
@event.listens_for(Test, 'after_insert')
def after_insert_test(mapper, connection, target):
    print("after_insert_test", file=sys.stdout)
    paciente = User.query.filter(User.id == target.id_paciente).first()
    medicos_asociados = paciente.medicos_asociados
    new_table = AccionesTestMedico.__table__
    for medico in medicos_asociados:
        data = {"num_test": target.num_test, "id_paciente": target.id_paciente, "id_medico": medico.id}
        connection.execute(new_table.insert(), data)
'''
'''
@event.listens_for(PacienteAsociado, 'after_insert')
def after_asociate_patient(mapper, connection, target):
    print('after asociate patient', file=sys.stderr)
    paciente = User.query.filter(User.id == target.id_paciente).first()
    tests = paciente.tests
    new_table = AccionesTestMedico.__table__
    for test in tests:
        data = {"num_test": test.num_test, "id_paciente": target.id_paciente, "id_medico": target.id_medico}
        connection.execute(new_table.insert(), data)
'''
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

from sqlalchemy.schema import DDL

trigger = DDL('''\
CREATE TRIGGER after_test_insert
AFTER INSERT
ON test FOR EACH ROW
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE id_medico_ INT;
    DECLARE cur CURSOR FOR SELECT id_medico FROM pacientes_asociados WHERE id_paciente = NEW.id_paciente;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
        medicos_loop: LOOP
            FETCH cur INTO id_medico_;
            IF done THEN
                LEAVE medicos_loop;
            END IF;
            INSERT INTO acciones_test_medico(num_test, id_paciente, id_medico, visto) values (NEW.num_test, NEW.id_paciente, id_medico_, FALSE);
        END LOOP;
    CLOSE cur;
END''')
event.listen(Test.__table__, 'after_create', trigger)


def create_data():
    from apps import user_datastore
    user_datastore.find_or_create_role(
        name="admin",
        permissions={"datos-personales-pacientes-centro", "datos-personales-personal-centro"},
    )

    user_datastore.find_or_create_role(
        name="admin-centro",
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
            identificador="46954321F",username="admin", email="admin@kruay.com", 
            password=hash_password("admin"), roles=["admin"]
        )
    
    if not user_datastore.find_user(username="auxiliar"):
        user_datastore.create_user(
            identificador="46654321R",username="auxiliar", email="webapptest2022@gmail.com", centro = centro1,
            password=hash_password("auxiliar"), nombre="auxiliar", roles=["auxiliar"]
        )

    if not user_datastore.find_user(username="auxiliar2"):
        user_datastore.create_user(
            identificador="35954651F",username="auxiliar2", email="auxiliar@kruay.com", centro = centro2,
            password=hash_password("auxiliar2"), nombre="auxiliar2", roles=["auxiliar"]
        )
    
    if not user_datastore.find_user(username="paciente11"):
        user_datastore.create_user(
            identificador="54354321R",username="paciente11", email="paciente11@kruay.com", centro = centro1,
            sexo="V", altura=1.79, peso=97, antecedentes_clinicos="diabetis",
            password=hash_password("paciente11"),nombre="paciente11", roles=["paciente"]
        )
    
    if not user_datastore.find_user(username="paciente12"):
        user_datastore.create_user(
            identificador="46953125F",username="paciente12", email="paciente12@kruay.com", centro = centro1,
            sexo="M", altura=1.56, peso=57, antecedentes_clinicos="cancer de mama",
            password=hash_password("paciente12"), nombre="paciente12", roles=["paciente"]
        )
    
    if not user_datastore.find_user(username="paciente21"):
        user_datastore.create_user(
            identificador="75954321F",username="paciente21", email="paciente21@kruay.com", centro = centro2,
            sexo="V", altura=1.91, peso=75, antecedentes_clinicos="cancer de pulmon, cancer de prostata, problemas hepaticos",
            password=hash_password("paciente21"),nombre="paciente21", roles=["paciente"]
        )
    
    paciente11 = user_datastore.find_user(username="paciente11")
    paciente21 = user_datastore.find_user(username="paciente21")
    if not user_datastore.find_user(username="medico"):
        user_datastore.create_user(
            identificador="98957621F",username="medico", email="medico@kruay.com", centro = centro1,
            password=hash_password("medico"), roles=["medico"], nombre="medico",
            pacientes_asociados=[paciente11, paciente21]
        )
    if not user_datastore.find_user(username="medico1"):
        user_datastore.create_user(
            identificador="52354321R",username="medico1", email="medico1@kruay.com", centro = centro1,
            password=hash_password("medico1"), roles=["medico"], nombre="medico1"
        )  

    if not user_datastore.find_user(username="medico2"):
        user_datastore.create_user(
            identificador="89354321F",username="medico2", email="medico2@kruay.com", centro = centro2,
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

def drop_all():
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base(bind=db.engine)
    Base.metadata.drop_all(bind=db.engine)
