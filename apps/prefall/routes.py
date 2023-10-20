from sqlite3 import IntegrityError
from sqlalchemy import null, desc, create_engine, exc, cast
import sqlalchemy

from io import BytesIO

from apps.authentication.models import AccionesTestMedico, DocumentoPaciente, PacienteAsociado, Role, Test, TestUnit, User, Centro, File, Model, Boundary, TrainingPoint
from apps.prefall import blueprint
from flask import abort, jsonify, render_template, request, redirect, url_for, send_file, session
from jinja2 import TemplateNotFound

from flask_security import (
    auth_required,
    roles_accepted,
    hash_password,
    current_user
)
from random import randint

from flask import flash, current_app, Response, send_from_directory
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import datetime

from apps.prefall.decorators import ( 
    admin_centro_access, 
    clinical_data_access, 
    patient_data_access, 
    personal_data_access,
    admin_centro_access_user
)
from apps.prefall.forms import (
    CreateCenterAdminForm,
    CreateCenterForm,
    CreatePatientClinicalForm,
    CreatePatientPersonalForm,
    CreateUserForm,
    DiagnosticarTestForm,
    EditCenterDataForm, 
    EditClinicalDataForm, 
    EditPersonalDataForm,
    FilterFileForm,
    FilterTestForm,
    FilterUserForm,
    UploadFileForm,
    UploadTestForm,
    ElementForm,
    ElementStringForm,
    DoubleElementForm,
    CompareTestsForm,
    CompareFasesForm,
    CompareTestsFormPaciente,
    CompareFasesFormPaciente,
    MetricForm
)

import csv
import pandas as pd
import json

from flask_ckeditor import upload_fail, upload_success


### BEGIN ADMIN ###

@blueprint.route('crear_centro', methods=['GET', 'POST'])
@roles_accepted("admin")
def crear_centro():
    form = CreateCenterForm(request.form)
    if 'create_center' in request.form and form.validate():

        # read form data
        cif = request.form['cif']
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        CP = request.form['CP']
        ciudad = request.form['ciudad']
        provincia = request.form['provincia']
        pais = request.form['pais']

        from apps import db
        centro = Centro(
            cif = cif, nombreFiscal = nombre, direccion=direccion, CP=CP, ciudad=ciudad,
            provincia=provincia, pais=pais)
        db.session.add(centro)
        db.session.commit()

        return redirect(url_for('home_blueprint.index'))


    return render_template('prefall/create_center.html', form=form)


@blueprint.route('/lista_centros', methods=['GET', 'POST'])
@roles_accepted("admin")
def lista_centros():
    from apps import db
    from apps.authentication.models import Centro

    centros = Centro.query.order_by(Centro.nombreFiscal).all()

    centros_data = [
        {"id": centro.id, "nombreFiscal": centro.nombreFiscal
        }for centro in centros]
    

    return render_template(
        'prefall/center_list.html', centros=centros, 
        centros_data=centros_data)


@blueprint.route('detalles_centro_admin/<id>', methods=['GET', 'POST'])
@roles_accepted("admin")
def detalles_centro_admin(id):
    from apps import db
    centro = Centro.query.filter_by(id=id).first()
    users = User.query.filter_by(id_centro=id).filter(Centro.id == id).\
        filter(db.or_(Centro.id_admin == None,Centro.id_admin != User.id)).all()
    users_data = [{"id": user.id, "apellidos": user.apellidos, "role": user.roles[0].name, 
        "nombre": user.nombre, "identificador": user.identificador, "fecha_nacimiento":user.fecha_nacimiento,
        } for user in users]
    admin = User.query.filter_by(id_centro=id).filter(Centro.id == id).\
        filter(Centro.id_admin == User.id).first()

    return render_template(
        'prefall/detalles_centro_admin.html', centro=centro,
        users_data=users_data, admin=admin)


@blueprint.route('crear_admin_centro/<id>', methods=['GET', 'POST'])
@roles_accepted("admin")
def crear_admin_centro(id):
    centro = Centro.query.filter_by(id=id).first()
    form = CreateCenterAdminForm()
    if form.validate_on_submit():
        identificador = form['identificador'].data
        nombre = form['nombre'].data
        apellidos = form['apellidos'].data
        fecha = form['fecha'].data
        sexo = form['sexo'].data
        password = form['password'].data
        username = form['username'].data
        email = form['email'].data
        from apps import user_datastore, db
        user_datastore.create_user(
            identificador=identificador, nombre=nombre, apellidos=apellidos, fecha_nacimiento=fecha, 
            sexo=sexo, id_centro = id, username=username,
            password=hash_password(password), email=email, roles=["admin-centro"]
        )
        user_created = User.query.filter_by(email=email).first()
        centro.id_admin = user_created.id
        db.session.add(centro)
        db.session.commit()

        return redirect(url_for('prefall_blueprint.detalles_centro', id_centro=id))

    return render_template(
        'prefall/create_admin_center.html', centro= centro, form=form
    )

@blueprint.route('editar_detalles_usuario/<id>', methods=['GET', 'POST'])
@admin_centro_access_user()
def editar_detalles_usuario(id):
    paciente = User.query.filter_by(id=id).first()
    form = EditPersonalDataForm(request.form)
    if 'editar_detalles_personales' in request.form and form.validate():
        identificador = request.form['identificador']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        fecha = request.form['fecha']
        sexo = request.form['sexo']
        altura = request.form['altura']
        peso = request.form['peso']
        password = form.password.data
        if identificador != "":
            paciente.identificador = identificador
        if nombre != "":
            paciente.nombre = nombre
        if apellidos != "":
            paciente.apellidos = apellidos
        if fecha != "":
            paciente.fecha_nacimiento = fecha
        if sexo != "":
            paciente.sexo = sexo
        if altura != "":
            paciente.altura = altura
        if peso != "":
            paciente.peso = peso
        if password != "":
            paciente.password = hash_password(password)
        from apps import db
        db.session.commit()
        return redirect(url_for('home_blueprint.index'))
        
    return render_template(
        'prefall/editar_detalles_personales.html', 
        form=form, paciente=paciente)

@blueprint.route('borrar_usuario/<id>', methods=['POST'])
@admin_centro_access_user()
def borrar_usuario(id):
    from apps import db
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"error": "User not found"}), 404


@blueprint.route('borrar_centro/<id>', methods=['POST'])
@admin_centro_access_user()
def borrar_centro(id):
    from apps import db
    centro = Centro.query.get(id)
    if centro:
        if len(centro.usuarios) == 0:
            db.session.delete(centro)
            db.session.commit()
            return jsonify({"message": "Centro deleted successfully"})
        else:
            return jsonify({"error": "El centro no esta vacio. Debes eliminar primero todos sus usuarios"}), 404
    return jsonify({"error": "Centro not found"}), 404

### END ADMIN ###

### BEGIN ADMIN CENTRO ###

@blueprint.route('detalles_centro/<id_centro>', methods=['GET', 'POST'])
@admin_centro_access()
def detalles_centro(id_centro):
    if current_user.has_role("admin"):
        return redirect(url_for("prefall_blueprint.detalles_centro_admin", id=id_centro))

    from apps import db
    centro = Centro.query.filter_by(id=id_centro).first()
    admin_centro_role = Role.query.filter_by(name="admin-centro").first()
    users = User.query.filter_by(id_centro=id_centro).\
        filter(db.not_(User.roles.contains(admin_centro_role))).all()
    users_data = [{"id": user.id, "apellidos": user.apellidos, "role": user.roles[0].name, 
        "nombre": user.nombre, "identificador": user.identificador, "fecha_nacimiento":user.fecha_nacimiento,
        } for user in users]

    return render_template(
        'prefall/detalles_centro.html', centro=centro, users_data=users_data)


@blueprint.route('borrar_admin/<id_centro>/<id_user>', methods=['GET','POST'])
@admin_centro_access()
def borrar_admin(id_centro, id_user):
    from apps import db, user_datastore
    user = User.query.filter_by(id=id_user).filter_by(id_centro=id_centro).first()
    if user.has_role("admin_centro") and current_user.has_role("admin_centro"):
        abort(403)

    else:
        user_datastore.delete_user(user)

        db.session.commit()

        return redirect(url_for("prefall_blueprint.detalles_centro", id_centro=id_centro))


@blueprint.route('editar_detalles_centro/<id_centro>', methods=['GET', 'POST'])
@admin_centro_access()
def editar_detalles_centro(id_centro):
    centro = Centro.query.filter_by(id=id_centro).first()
    form = EditCenterDataForm(request.form)
    if 'editar_detalles_centro' in request.form and form.validate():
        cif = request.form['cif']
        nombreFiscal = request.form['nombreFiscal']
        direccion = request.form['direccion']
        CP = request.form['CP']
        ciudad = request.form['ciudad']
        provincia = request.form['provincia']
        pais = request.form['pais']
        if cif != "":
            centro.cif = cif
        if nombreFiscal != "":
            centro.nombreFiscal = nombreFiscal
        if direccion != "":
            centro.direccion = direccion
        if CP != "":
            centro.CP = CP
        if ciudad != "":
            centro.ciudad = ciudad
        if provincia != "":
            centro.provincia = provincia
        if pais != "":
            centro.pais = pais
        from apps import db
        db.session.commit()
        return redirect(url_for('prefall_blueprint.detalles_centro', id_centro=id_centro))
        
    return render_template(
        'prefall/editar_detalles_centro.html', 
        form=form, centro=centro)


@blueprint.route('crear_user', methods=['GET', 'POST'])
@roles_accepted("admin-centro")
def crear_user():
    create_user_form = CreateUserForm(request.form)
    if 'create_user' in request.form and create_user_form.validate():

        # read form data
        identificador = request.form['identificador']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        fecha = request.form['fecha']
        sexo = request.form['sexo']
        role = create_user_form.tipo.data
        password = request.form['password']
        username = request.form['username']
        email = request.form['email']

        if role == 'paciente':
            altura = request.form['altura']
            peso = request.form['peso']
        else:
            altura = None
            peso = None

        from apps import user_datastore, db
        user_datastore.create_user(
            identificador=identificador, nombre=nombre, apellidos=apellidos, fecha_nacimiento=fecha, 
            sexo=sexo, altura=altura, peso=peso, id_centro = current_user.id_centro, username=username,
            password=hash_password(password), email=email, roles=[role]
        )
        db.session.commit()

        return redirect(url_for('home_blueprint.index'))


    return render_template('prefall/create_user.html', form=create_user_form)
### END ADMIN CENTRO ###

### BEGIN MEDICO ###

@blueprint.route('/pantalla_principal_medico', methods=['GET', 'POST'])
@roles_accepted("medico")
def pantalla_principal_medico():
    from apps import db
    from datetime import datetime
    from sqlalchemy import and_, func, select, literal, case
    from sqlalchemy.orm import joinedload
    from sqlalchemy.orm import aliased
    formPacientes = FilterUserForm()
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of items per page

    test_sin_diagnosticar_subquery = (
        select([
            User.id.label('id_paciente'),
            func.count().label('tests_sin_diagnostico')
        ])
        .select_from(User)
        .join(AccionesTestMedico, User.id == AccionesTestMedico.id_paciente)
        .join(Test, and_(
            AccionesTestMedico.num_test == Test.num_test,
            AccionesTestMedico.id_paciente == Test.id_paciente
        ))
        .filter(AccionesTestMedico.id_medico == current_user.id)
        .filter(AccionesTestMedico.diagnostico.is_(None))
        .group_by(User.id)
        .alias()
    )

    test_sin_revisar_subquery = (
        select([
            User.id.label('id_paciente'),
            func.count().label('tests_sin_revisar')
        ])
        .select_from(User)
        .join(AccionesTestMedico, User.id == AccionesTestMedico.id_paciente)
        .join(Test, and_(
            AccionesTestMedico.num_test == Test.num_test,
            AccionesTestMedico.id_paciente == Test.id_paciente
        ))
        .filter(AccionesTestMedico.id_medico == current_user.id)
        .filter(Test.probabilidad_caida.is_(None))
        .group_by(User.id)
        .alias()
    )

    pacientes = (
        current_user.pacientes_asociados
        .join(test_sin_diagnosticar_subquery, test_sin_diagnosticar_subquery.c.id_paciente == User.id, isouter=True)
        .join(test_sin_revisar_subquery, test_sin_revisar_subquery.c.id_paciente == User.id, isouter=True)
        .with_entities(
            User,
            case([(test_sin_diagnosticar_subquery.c.tests_sin_diagnostico.is_(None), literal(0))],
             else_=test_sin_diagnosticar_subquery.c.tests_sin_diagnostico).label('diagnosticos_pendientes'),
            case([(test_sin_revisar_subquery.c.tests_sin_revisar.is_(None), literal(0))],
             else_=test_sin_revisar_subquery.c.tests_sin_revisar).label('revisiones_pendientes'),

        )
        .all()
    )

    pacientes_data = [{"id": paciente.User.id, "apellidos": paciente.User.apellidos, 
        "centro": paciente.User.centro.nombreFiscal, "nombre": paciente.User.nombre, 
        "identificador": paciente.User.identificador, "fecha_registro":paciente.User.create_datetime,
        "tests_sin_diagnostigar": paciente.diagnosticos_pendientes, "tests_sin_revisar": paciente.revisiones_pendientes
        } for paciente in pacientes]
    total_records = len(pacientes)

    total_pages = (total_records - 1) // per_page + 1

    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, total_records)

    pacientes = pacientes[start_index:end_index]

    id_asociados = [pa.id for pa in current_user.pacientes_asociados]

    Medico = aliased(User)

    test_sin_diagnosticar = current_user.tests_de_pacientes.\
        join(User, AccionesTestMedico.id_paciente == User.id).\
        join(Test, db.and_(AccionesTestMedico.num_test == Test.num_test, 
            AccionesTestMedico.id_paciente == Test.id_paciente)).\
        outerjoin(Medico, Test.id_medico == User.id).\
        with_entities(
            AccionesTestMedico.visto, 
            AccionesTestMedico.diagnostico, 
            User.nombre.label('nombre_paciente'),
            User.id.label('id_paciente'),
            AccionesTestMedico.num_test, 
            Test.date, 
            Medico.nombre.label('nombre_medico'),
            Medico.apellidos.label('apellidos_medico')
        ).filter(AccionesTestMedico.diagnostico == None).all()

    test_sin_diagnosticar_list = [
        {
            "visto": item[0],
            "diagnostico": item[1],
            "nombre_paciente": item[2],
            "id_paciente": item[3],
            "num_test": item[4],
            "date": item[5].strftime('%Y-%m-%d %H:%M:%S'),
            "nombre_medico": item[6],
            "apellidos_medico": item[7]
        }
        for item in test_sin_diagnosticar
    ]
    
    test_sin_revisar = current_user.tests_de_pacientes.\
        join(User, AccionesTestMedico.id_paciente == User.id).\
        join(Test, db.and_(AccionesTestMedico.num_test == Test.num_test, 
            AccionesTestMedico.id_paciente == Test.id_paciente)).\
        outerjoin(Medico, Test.id_medico == User.id).\
        with_entities(
            AccionesTestMedico.visto, 
            AccionesTestMedico.diagnostico, 
            User.nombre.label('nombre_paciente'),
            User.id.label('id_paciente'),
            AccionesTestMedico.num_test, 
            Test.date, 
            Medico.nombre.label('nombre_medico'),
            Medico.apellidos.label('apellidos_medico')
        ).filter(Test.probabilidad_caida == None).all()

    test_sin_revisar_list = [
        {
            "visto": item[0],
            "diagnostico": item[1],
            "nombre_paciente": item[2],
            "id_paciente": item[3],
            "num_test": item[4],
            "date": item[5].strftime('%Y-%m-%d %H:%M:%S'),
            "nombre_medico": item[6],
            "apellidos_medico": item[7]
        }
        for item in test_sin_revisar
    ]

    return render_template(
        'prefall/pantalla_principal_medico.html', pacientes=pacientes, pacientes_data=pacientes_data,
        test_sin_diagnosticar=test_sin_diagnosticar_list, test_sin_revisar=test_sin_revisar_list,
        total_pages=total_pages, current_page=page)

@blueprint.route('crear_paciente_medico', methods=['GET', 'POST'])
@roles_accepted("medico")
def crear_paciente_medico():
    create_patient_form = CreatePatientClinicalForm(request.form)
    if 'create_patient' in request.form and create_patient_form.validate():

        # read form data
        identificador = request.form['identificador']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        fecha = request.form['fecha']
        sexo = request.form['sexo']
        altura = request.form['altura']
        peso = request.form['peso']
        antecedentes = request.form['antecedentes']
        password = request.form['password']
        username = request.form['username']
        email = request.form['email']

        from apps import user_datastore, db
        user_datastore.create_user(
            identificador=identificador, nombre=nombre, apellidos=apellidos, 
            fecha_nacimiento=fecha, sexo=sexo, altura=altura,
            peso=peso, antecedentes_clinicos=antecedentes, id_centro = current_user.id_centro,
            password=hash_password(password), email=email, roles=["paciente"], username=username
        )
        user_created = User.query.filter_by(identificador=identificador).first()
        asociacion = PacienteAsociado(id_paciente= user_created.id, id_medico=current_user.id)
        db.session.add(asociacion)
        db.session.commit()

        return redirect(url_for('home_blueprint.index'))


    return render_template('prefall/create_patient_clinical.html', form=create_patient_form)

@blueprint.route('detalles_test/<id>/<num>', defaults={"editing": False}, methods=['GET', 'POST'])
@blueprint.route('detalles_test/<id>/<num>/<editing>', methods=['GET', 'POST'])
@clinical_data_access()
def detalles_test(id, num, editing):
    from apps import db
    test = db.session.query(Test, AccionesTestMedico).\
        join(Test, db.and_(AccionesTestMedico.num_test == Test.num_test, 
        AccionesTestMedico.id_paciente == Test.id_paciente)).\
            with_entities(AccionesTestMedico.visto, AccionesTestMedico.diagnostico, Test.num_test, 
            Test.date, Test.id_paciente, Test.id_centro, Test.probabilidad_caida).\
                        filter(AccionesTestMedico.id_medico == current_user.id).\
                            filter(Test.id_paciente == id).\
                                filter(Test.num_test == num).first()

    if not test.visto:
        db.session.query(AccionesTestMedico).filter_by(num_test=num).filter_by(id_paciente=id).\
            filter_by(id_medico=current_user.id).update({"visto": True})
        db.session.commit()
    form = DiagnosticarTestForm()
    if form.submitDiagnosticoTest.data and form.validate():
        db.session.query(AccionesTestMedico).filter_by(num_test=num).filter_by(id_paciente=id).\
            filter_by(id_medico=current_user.id).update({"diagnostico": form.diagnostico.data})
        db.session.commit()
        test = db.session.query(Test, AccionesTestMedico).\
            join(Test, db.and_(AccionesTestMedico.num_test == Test.num_test, 
            AccionesTestMedico.id_paciente == Test.id_paciente)).\
                with_entities(AccionesTestMedico.visto, AccionesTestMedico.diagnostico, Test.num_test, 
                Test.date, Test.id_paciente, Test.id_centro, Test.probabilidad_caida).\
                            filter(AccionesTestMedico.id_medico == current_user.id).\
                                filter(Test.id_paciente == id).\
                                    filter(Test.num_test == num).first()
        editing = False
    elif editing:
        form.diagnostico.data = test.diagnostico

    test_data = {
            "num_test": test.num_test,
            "id_paciente": test.id_paciente,
        }
    '''
    if test.bow is not None:
        from apps.authentication.models import GraphJson
        import time
        startTime = time.time()
        SERIALIZE_GRAPH = False
        if SERIALIZE_GRAPH:
            graphJSON = db.session.query(GraphJson.graph).filter_by(num_test=num).filter_by(id_paciente=id).first()[0]
            if graphJSON is None:
                graphJSON = generatePlot(id, num)
                graphDB = GraphJson(id_paciente=id, num_test=num, graph=graphJSON)
                db.session.add(graphDB)
                db.session.commit()
        else:
            graphJSON = generatePlot(id, num)
        import sys
        print(time.time() - startTime, file=sys.stderr)
        return render_template(
            'prefall/detalles_test.html', form = form, test = test, editing = editing, graphJSON=graphJSON
        )
    else:
        return render_template(
            'prefall/detalles_test.html', form = form, test = test, editing = editing
        )
    '''
    return render_template(
        'prefall/detalles_test.html', form = form, test = test, editing = editing, test_data = test_data
    )

def Average(lst):
    return sum(lst) / len(lst)


def generatePlotPaciente(id_paciente):
    from apps import db
    import plotly
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import pickle
    import math
    import numpy as np
    tests = db.session.query(
        Test.num_test, Test.date, Test.probabilidad_caida, Test.data)\
        .filter_by(id_paciente=id_paciente)\
        .filter(Test.probabilidad_caida.isnot(None)).all()

    dataframes = []

    for test in tests:
        blob_data = test.data  
        if blob_data:
            df = pickle.loads(blob_data)
            dataframes.append(df)
    
    x = [test.date for test in tests]
    y = [test.probabilidad_caida for test in tests]
    
    fig = make_subplots(
        rows=3, cols=1,
        specs=[[{'type': 'scatter'}], [{'type': 'scatter3d'}], [{'type': 'bar'}]],
        subplot_titles=('Probability of Fall Over Time', 'Probability of Fall depending on lacc', 'Comparasion lacc'),
        row_heights=[600, 1000, 600],
    )
    
    trace = go.Scatter(x=x, y=y, mode='lines+markers')

    fig.add_trace(trace, row=1, col=1)

    fig.update_xaxes(title_text='Date', row=1, col=1)
    fig.update_yaxes(title_text='Probability of Falling', range=[0, 1], row=1, col=1)


    x = []
    for df in dataframes:
        mean = (df['lax_mean_f1'] * df['duracion_f1']\
        + df['lax_mean_f2'] * df['duracion_f2']\
        + df['lax_mean_f3'] * df['duracion_f3']\
        + df['lax_mean_f4'] * df['duracion_f4'])\
        / (df['duracion_f1'] + df['duracion_f2'] + df['duracion_f3'] + df['duracion_f4'])
        x.append(mean.values[0])

    y = []
    for df in dataframes:
        mean = (df['lay_mean_f1'] * df['duracion_f1']\
        + df['lay_mean_f2'] * df['duracion_f2']\
        + df['lay_mean_f3'] * df['duracion_f3']\
        + df['lay_mean_f4'] * df['duracion_f4'])\
        / (df['duracion_f1'] + df['duracion_f2'] + df['duracion_f3'] + df['duracion_f4'])
        y.append(mean.values[0])

    z = []
    for df in dataframes:
        mean = (df['laz_mean_f1'] * df['duracion_f1']\
        + df['laz_mean_f2'] * df['duracion_f2']\
        + df['laz_mean_f3'] * df['duracion_f3']\
        + df['laz_mean_f4'] * df['duracion_f4'])\
        / (df['duracion_f1'] + df['duracion_f2'] + df['duracion_f3'] + df['duracion_f4'])
        z.append(mean.values[0])

    c = [test.probabilidad_caida for test in tests]

    trace = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=5, 
            color=c, 
            colorscale='Viridis', 
            colorbar=dict(len=0.3, y=0.35, yanchor='bottom'),  
            opacity=1, 
        )
    )

    fig.add_trace(trace, row=2, col=1)

    fig.update_scenes(xaxis_title='Linear Acc X', yaxis_title='Linear Acc Y', zaxis_title='Linear Acc Z', row=2, col=1)
    
    x_floor = math.floor(min(x))
    x_ceil = math.ceil(max(x))

    y_floor = math.floor(min(y))
    y_ceil = math.ceil(max(y))

    z_floor = math.floor(min(z))
    z_ceil = math.ceil(max(z))

    fig.update_layout(scene=dict(
        xaxis=dict(range=[x_floor, x_ceil]),
        yaxis=dict(range=[y_floor, y_ceil]),
        zaxis=dict(range=[z_floor, z_ceil]),
    ))

    if len(x) >= 2:
        labels = ["Linear Acc X", "Linear Acc Y", "Linear Acc Z"]
        bars1 = [x[0], y[0], z[0]]
        bars2 = [x[1], y[1], z[1]]
        trace_group1 = go.Bar(x=labels, y=bars1, name='Paciente 1', text=bars1, textposition='outside')
        trace_group2 = go.Bar(x=labels, y=bars2, name='Paciente 2', text=bars2, textposition='outside')

        fig.add_trace(trace_group1, row=3, col=1)
        fig.add_trace(trace_group2, row=3, col=1)

        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside', selector=dict(type='bar'))


    fig.update_layout(
        autosize=False,
        height=2400,  # Adjust the height as needed
        margin=dict(l=50, r=50, b=50, t=50),
    )


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON



def generatePlot(id_paciente, num_test):
    from apps import db
    query_boundary = db.session.query(
        Boundary.intercept, Boundary.coef0, Boundary.coef1,Boundary.coef2).\
        filter(Test.num_test == num_test).\
        filter(Test.id_paciente == id_paciente).\
        filter(Test.model == Boundary.model)
    df_boundary = pd.read_sql(query_boundary.statement, db.session.bind)
    query_train = db.session.query(
        TrainingPoint.clase, TrainingPoint.acc_x, TrainingPoint.acc_y,TrainingPoint.acc_z).\
        filter(Test.num_test == num_test).\
        filter(Test.id_paciente == id_paciente).\
        filter(Test.model == TrainingPoint.model)
    df_train = pd.read_sql(query_train.statement, db.session.bind)
    query_test = db.session.query(
        Test.num_test, Test.id_paciente, Test.date, TestUnit.item, TestUnit.time, TestUnit.acc_x,
        TestUnit.acc_y, TestUnit.acc_z, TestUnit.gyr_x, TestUnit.gyr_y, TestUnit.gyr_z,
        TestUnit.mag_x, TestUnit.mag_y, TestUnit.mag_z).\
                        filter(Test.id_paciente == TestUnit.id_paciente).\
                            filter(Test.num_test == TestUnit.num_test).\
                                filter(Test.id_paciente==id_paciente).\
                                    filter(Test.num_test==num_test)
    df_test = pd.read_sql(query_test.statement, db.session.bind)
    import plotly
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    test = Test.query.filter_by(num_test=num_test).filter_by(id_paciente=id_paciente).first()
    probabilidades = [["Bow", test.bow, "Bow"], ["Fall-to-left", test.fall_to_left, "Fall to left"], 
    ["Fall-to-right", test.fall_to_right, "Fall to right"], ["Falling-backward", test.falling_backward, "Falling backward"], 
    ["Falling-forward", test.falling_forward, "Falling forward"], ["Idle", test.idle, "Idle"], 
    ["Sitting", test.sitting, "Sitting"], ["Sleep", test.sleep, "Sleep"], ["Standing", test.standing, "Standing"]]
    probabilidades_ordenadas = probabilidades.copy()
    probabilidades_ordenadas.sort(key = lambda x: x[1], reverse=True)
    for index, po in enumerate(probabilidades_ordenadas):
        index2 = [i for i, p in enumerate(probabilidades) if po[0] == p[0]][0]
        probabilidades_ordenadas[index].append(index2)
    
    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=[prob_ord[2] + " " + str(round(prob_ord[1] * 100, 2)) + "%" for prob_ord in probabilidades_ordenadas],
        specs=[[{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}],
            [{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}],
            [{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}]])

    greyscale=[
        [0, "rgb(0, 0, 0)"],
        [0.1, "rgb(0, 0, 0)"],

        [0.1, "rgb(20, 20, 20)"],
        [0.2, "rgb(20, 20, 20)"],

        [0.2, "rgb(40, 40, 40)"],
        [0.3, "rgb(40, 40, 40)"],

        [0.3, "rgb(60, 60, 60)"],
        [0.4, "rgb(60, 60, 60)"],

        [0.4, "rgb(80, 80, 80)"],
        [0.5, "rgb(80, 80, 80)"],

        [0.5, "rgb(100, 100, 100)"],
        [0.6, "rgb(100, 100, 100)"],

        [0.6, "rgb(120, 120, 120)"],
        [0.7, "rgb(120, 120, 120)"],

        [0.7, "rgb(140, 140, 140)"],
        [0.8, "rgb(140, 140, 140)"],

        [0.8, "rgb(160, 160, 160)"],
        [0.9, "rgb(160, 160, 160)"],

        [0.9, "rgb(180, 180, 180)"],
        [1.0, "rgb(180, 180, 180)"]
    ]
    import numpy
    x = numpy.linspace(-1, 1, 10)
    y = numpy.linspace(-1, 1, 10)
    xGrid, yGrid = numpy.meshgrid(x, y)
    for i, po in enumerate(probabilidades_ordenadas):
        index = po[3]
        z = (-df_boundary["intercept"].iloc[index] - df_boundary["coef0"].iloc[index] * xGrid - df_boundary["coef1"].iloc[index] * yGrid) / df_boundary["coef2"].iloc[index]
        fig.add_trace(go.Surface(name="Boundary" , x=x, y=y, z=z, colorscale=greyscale, showscale=False),row=i // 3 + 1, col=i % 3 + 1)

        x_test = df_test["acc_x"] * 0.10197162129779
        y_test = df_test["acc_y"] * 0.10197162129779
        z_test = df_test["acc_z"] * 0.10197162129779

        fig.add_trace(go.Scatter3d(name="Test points", showlegend=i==0,x=x_test, y=y_test, z=z_test, mode ='markers', 
                                   marker = dict(
                                     size = 2,
                                     color ='rgb(230, 230, 0)',
                                     opacity = 0.8
                                   )), row=i // 3 + 1, col=i % 3 + 1)

        df_train_class = df_train[df_train["clase"] == po[0]]
        df_train_other_class = df_train[df_train["clase"] != po[0]]

        x_train_class = df_train_class["acc_x"]
        y_train_class = df_train_class["acc_y"]
        z_train_class = df_train_class["acc_z"]

        fig.add_trace(go.Scatter3d(name="Train points from class", showlegend=i==0, x=x_train_class, y=y_train_class, z=z_train_class, mode ='markers', 
                                   marker = dict(
                                     size = 2,
                                     color ='rgb(0, 230, 0)',
                                     opacity = 0.8
                                   )), row=i // 3 + 1, col=i % 3 + 1)

        x_train_other_class = df_train_other_class["acc_x"]
        y_train_other_class = df_train_other_class["acc_y"]
        z_train_other_class = df_train_other_class["acc_z"]

        fig.add_trace(go.Scatter3d(name="Train points from other classes" ,  showlegend=i==0, x=x_train_other_class, y=y_train_other_class, z=z_train_other_class, mode ='markers', 
                                   marker = dict(
                                     size = 2,
                                     color ='rgb(230, 0, 0)',
                                     opacity = 0.8
                                   )), row=i // 3 + 1, col=i % 3 + 1)

        if i == 0:
            scene_num = "scene"
        else:
            scene_num = "scene" + str(i + 1)
        fig.layout[scene_num]["annotations"] = [
            dict(
                x = Average(x_test),
                y = Average(y_test),
                z = Average(z_test),
                text = "Test data",
                font=dict(
                    color="black",
                    size=8
                ),
            ),
            dict(
                x = Average(x_train_class),
                y = Average(y_train_class),
                z = Average(z_train_class),
                text = "Train data from class",
                font=dict(
                    color="black",
                    size=8
                ),
            ),
            dict(
                x = Average(x_train_other_class),
                y = Average(y_train_other_class),
                z = Average(z_train_other_class),
                text = "Train data from other classes",
                font=dict(
                    color="black",
                    size=8
                ),
            )
        ]
    fig.update_layout(
        height=1600,
        width=1600
    )
    print(fig.layout)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

    

@blueprint.route('detalles_clinicos/<id>', methods=['GET', 'POST'])
@clinical_data_access()
def detalles_clinicos(id):
    from apps import db
    from sqlalchemy.orm import joinedload
    from sqlalchemy import and_
    paciente = User.query.filter_by(id=id).first()
    formTest = UploadTestForm()
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of items per page

    if formTest.submitUploadTest.data and formTest.validate():
        file = formTest.test.data
        filename = secure_filename(file.filename)
        Path(os.path.join(current_app.instance_path,current_app.config['UPLOAD_FOLDER'])).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(current_app.instance_path,current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        df = read_csv(file_path)
        df = add_columns(df, id)
        df = df.drop_duplicates(subset=["time"])
        add_df_to_sql(df, paciente.id_centro, filename)
        '''
        try:
            add_df_to_sql(df)
        except sqlalchemy.exc.IntegrityError:
            form.test.errors.append("Duplicated data")
        '''

        os.remove(file_path)
    
    tests = (
        db.session.query(Test, AccionesTestMedico)
        .join(User, User.id == Test.id_paciente)
        .join(
            AccionesTestMedico,
            and_(
                AccionesTestMedico.num_test == Test.num_test,
                AccionesTestMedico.id_paciente == Test.id_paciente,
                AccionesTestMedico.id_medico == current_user.id  
            )
        )
        .filter(Test.id_paciente == id)
        .options(joinedload(Test.medico))
        .all()
    )
    total_records = len(tests)

    total_pages = (total_records - 1) // per_page + 1

    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, total_records)

    tests = tests[start_index:end_index]    

    #graphJSON = generatePlotPaciente(id)
    graphJSON = null

    print(tests)

    tests_data = [{"num_test": test.num_test, "date": test.date, 
    "medico": (test.medico.nombre + " " + test.medico.apellidos) if (test.medico and test.medico.apellidos is not None) else test.medico.nombre if test.medico else "", 
    "prob_caida": test.probabilidad_caida, "diagnostico": acciones_test_medico.diagnostico, 
    } for test, acciones_test_medico in tests]

    return render_template('prefall/detalles_clinicos.html', paciente=paciente, tests=tests,
    formTest=formTest, graphJSON=graphJSON, tests_data = tests_data,
    total_pages=total_pages, current_page=page)


@blueprint.route('/editar_paciente/<int:id>', methods=['POST'])
@clinical_data_access()
def editar_paciente(id):
    from apps import db
    paciente = User.query.get(id)
    
    if paciente is None:
        return jsonify({'error': 'Paciente no encontrado'}), 404

    nuevo_valor = request.form['nuevo_valor']
    campo_editado = request.form['campo_editado']

    if campo_editado == 'nombre':
        paciente.nombre = nuevo_valor
    elif campo_editado == 'apellidos':
        paciente.apellidos = nuevo_valor
    elif campo_editado == 'identificador':
        paciente.identificador = nuevo_valor
    elif campo_editado == 'sexo':
        paciente.sexo = nuevo_valor
    elif campo_editado == 'centro':
        centro = Centro.query.filter_by(id=nuevo_valor).first()
        if centro:
            paciente.id_centro = centro.id 
            db.session.commit()
            return jsonify({"nuevo_valor": centro.nombreFiscal})
        else:
            return jsonify({"error": "Centro no encontrado"}), 404
    elif campo_editado == "password":
        paciente.password = hash_password(nuevo_valor)
    else:
        return jsonify({'error': 'Campo no válido'}), 400

    db.session.commit()

    return jsonify({'nuevo_valor': nuevo_valor})


@blueprint.route('editar_detalles_clinicos/<id>', methods=['GET', 'POST'])
@clinical_data_access()
def editar_detalles_clinicos(id):
    paciente = User.query.filter_by(id=id).first()
    form = EditClinicalDataForm(request.form)
    if 'editar_detalles_clinicos' in request.form and form.validate():
        identificador = request.form['identificador']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        fecha = request.form['fecha']
        sexo = request.form['sexo']
        altura = request.form['altura']
        peso = request.form['peso']
        antecedentes = request.form['antecedentes']
        if identificador != "":
            paciente.identificador = identificador
        if nombre != "":
            paciente.nombre = nombre
        if apellidos != "":
            paciente.apellidos = apellidos
        if fecha != "":
            paciente.fecha_nacimiento = fecha
        if sexo != "":
            paciente.sexo = sexo
        if altura != "":
            paciente.altura = altura
        if peso != "":
            paciente.peso = peso
        if antecedentes != "":
            paciente.antecedentes_clinicos = antecedentes
        from apps import db
        db.session.commit()
        return redirect(url_for('prefall_blueprint.detalles_clinicos', id=id))
        
    return render_template(
        'prefall/editar_detalles_clinicos.html', 
        form=form, paciente=paciente)

@blueprint.route('download_file/<file_id>')
def download_file(file_id):
    file = File.query.filter_by(id=file_id).first()
    return send_file(BytesIO(file.data), attachment_filename=file.filename, as_attachment=True)

@blueprint.route('guardar_analisis/<num_test>/<id_paciente>', methods=['POST'])
@clinical_data_access()
def guardar_analisis(num_test, id_paciente):
    from apps import db
    data = request.json
    import sys
    import pickle
    print(data, file=sys.stdout)
    result = data['result']
    probability = result['probability']
    model_id = result['model_id']
    df = pd.DataFrame([result['datos']])
    df_bytes = pickle.dumps(df)

    if db.session.query(Model.id).filter_by(id=model_id).first() is None: 
        model = Model(id = model_id)
        db.session.add(model)
        newModel = True
    else:
        newModel = False

    db.session.query(Test).filter_by(num_test=num_test).\
    filter_by(id_paciente=id_paciente).update({"probabilidad_caida": probability, 
    "model":model_id, "data":df_bytes})

    '''
    if newModel:  
        intercept = result['intercept']
        coef = result['coef']
        for i in range(len(intercept)):
            boundary = Boundary(model_id = model_id, index=i,
            intercept=intercept[i], coef0=coef[i][0], coef1=coef[i][1], coef2=coef[i][2])
            db.session.add(boundary)
        training_data = result['training_data']
        for key, value in training_data.items():
            import pandas
            df = pandas.read_json(value)
            for index, row in df.iterrows():
                training_point = TrainingPoint(model_id = model_id, index = index, clase = key, acc_x=row["Ax"],
                acc_y=row["Ay"], acc_z=row["Az"])
                db.session.add(training_point)
    '''

    db.session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@blueprint.route('plot_data/<num_test>/<id_paciente>', methods=['GET'])
def plot_data(num_test, id_paciente):
    from apps import db
    query_boundary = db.session.query(
        Boundary.intercept, Boundary.coef0, Boundary.coef1,Boundary.coef2).\
        filter(Test.num_test == num_test).\
        filter(Test.id_paciente == id_paciente).\
        filter(Test.model == Boundary.model)
    df_boundary = pd.read_sql(query_boundary.statement, db.session.bind)
    query_train = db.session.query(
        TrainingPoint.clase, TrainingPoint.acc_x, TrainingPoint.acc_y,TrainingPoint.acc_z).\
        filter(Test.num_test == num_test).\
        filter(Test.id_paciente == id_paciente).\
        filter(Test.model == TrainingPoint.model)
    df_train = pd.read_sql(query_train.statement, db.session.bind)
    query_test = db.session.query(
        Test.num_test, Test.id_paciente, Test.date, TestUnit.item, TestUnit.time, TestUnit.acc_x,
        TestUnit.acc_y, TestUnit.acc_z, TestUnit.gyr_x, TestUnit.gyr_y, TestUnit.gyr_z,
        TestUnit.mag_x, TestUnit.mag_y, TestUnit.mag_z).\
                        filter(Test.id_paciente == TestUnit.id_paciente).\
                            filter(Test.num_test == TestUnit.num_test).\
                                filter(Test.id_paciente==id_paciente).\
                                    filter(Test.num_test==num_test)
    df_test = pd.read_sql(query_test.statement, db.session.bind)
    data = {
        "intercept": df_boundary["intercept"].to_list(),
        "coef0": df_boundary["coef0"].to_list(),
        "coef1": df_boundary["coef1"].to_list(),
        "coef2": df_boundary["coef2"].to_list(),
        "acc_x_test": df_test["acc_x"].to_list(),
        "acc_y_test": df_test["acc_y"].to_list(),
        "acc_z_test": df_test["acc_z"].to_list(),
        "class_train": df_train["clase"].to_list(),
        "acc_x_train": df_train["acc_x"].to_list(),
        "acc_y_train": df_train["acc_y"].to_list(),
        "acc_z_train": df_train["acc_z"].to_list(),
    }
    return jsonify(data)


@blueprint.route('/borrar_test/<num_test>/<id_paciente>', methods=['POST'])
@clinical_data_access()
def borrar_test(num_test, id_paciente):
    from apps import db
    test = Test.query.filter_by(num_test=num_test, id_paciente=id_paciente).first()

    if test:
        db.session.delete(test)
        db.session.commit()
        return jsonify({'message': 'Test deleted successfully'}), 200
    else:
        return jsonify({'message': 'Test not found'}), 404

### END MEDICO ###
### BEGIN AUXILIAR ###

@blueprint.route('/pantalla_principal_auxiliar', methods=['GET', 'POST'])
@roles_accepted("auxiliar")
def pantalla_principal_auxiliar():
    from apps import db
    formPacientes = FilterUserForm()
    userRole = Role.query.filter_by(name="paciente").first()
    center = current_user.centro

    pacientes = User.query.\
        filter(User.roles.contains(userRole)).\
            filter_by(centro = center).all()
        
    pacientes_data = [{"id": paciente.id, "apellidos": paciente.apellidos, 
        "centro": paciente.centro.nombreFiscal, "nombre": paciente.nombre, 
        "identificador": paciente.identificador, "fecha_registro":paciente.create_datetime,
        } for paciente in pacientes]

    return render_template(
        'prefall/pantalla_principal_auxiliar.html', pacientes=pacientes,
        pacientes_data = pacientes_data, formPacientes=formPacientes)

@blueprint.route('crear_paciente', methods=['GET', 'POST'])
@roles_accepted("auxiliar")
def crear_paciente_auxiliar():
    create_patient_form = CreatePatientPersonalForm(request.form)
    if 'create_patient' in request.form and create_patient_form.validate():

        # read form data
        identificador = request.form['identificador']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        fecha = request.form['fecha']
        sexo = request.form['sexo']
        altura = request.form['altura']
        peso = request.form['peso']
        password = request.form['password']
        username = request.form['username']
        email = request.form['email']

        from apps import user_datastore, db
        user_datastore.create_user(
            identificador=identificador, nombre=nombre, apellidos=apellidos,
            fecha_nacimiento=fecha, sexo=sexo, altura=altura,
            peso=peso, id_centro = current_user.id_centro, username=username,
            password=hash_password(password), email=email, roles=["paciente"]
        )
        db.session.commit()

        return redirect(url_for('home_blueprint.index'))


    return render_template('prefall/create_patient_personal.html', form=create_patient_form)


@blueprint.route('detalles_personales/<id>', methods=['GET', 'POST'])
@personal_data_access()
def detalles_personales(id):
    from apps import db
    paciente = User.query.filter_by(id=id).first()
    medicos_asociados = paciente.medicos_asociados
    uploadTestForm = UploadTestForm()
    searchDoctorForm = FilterUserForm()

    if uploadTestForm.submitUploadTest.data and uploadTestForm.validate():
        file = uploadTestForm.test.data
        filename = secure_filename(file.filename)
        Path(os.path.join(current_app.instance_path,current_app.config['UPLOAD_FOLDER'])).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(current_app.instance_path,current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        df = read_csv(file_path)
        df = add_columns(df, id)
        df = df.drop_duplicates(subset=["time"])
        add_df_to_sql(df, paciente.id_centro, filename)
        os.remove(file_path)

    rolMedico = Role.query.filter_by(name="medico").first()
    id_asociados = [ma.id for ma in medicos_asociados]
    
    medicos = User.query.\
        filter(User.roles.contains(rolMedico)).\
            filter(db.not_(User.id.in_(id_asociados))).order_by(User.nombre).all()

    medicos_data = [{"id": medico.id, "apellidos": medico.apellidos, 
        "centro": medico.centro.nombreFiscal, "nombre": medico.nombre, 
        "identificador": medico.identificador, "fecha_registro":medico.create_datetime,
        } for medico in medicos]

    medicos_asociados_data = [{"id": medico.id, "apellidos": medico.apellidos, 
        "centro": medico.centro.nombreFiscal, "nombre": medico.nombre, 
        "identificador": medico.identificador, "fecha_registro":medico.create_datetime,
        } for medico in medicos_asociados]

    tests = Test.query.filter_by(id_paciente=id).all()

    tests_data = [{"num_test": test.num_test, "date":test.date
        } for test in tests]

    return render_template(
        'prefall/detalles_personales.html', paciente=paciente, tests_data=tests_data,
        medicos_data=medicos_data, medicos_asociados_data=medicos_asociados_data,
         tests=tests, uploadTestForm=uploadTestForm, searchDoctorForm=searchDoctorForm)


@blueprint.route('editar_detalles_personales/<id>', methods=['GET', 'POST'])
@personal_data_access()
def editar_detalles_personales(id):
    paciente = User.query.filter_by(id=id).first()
    form = EditPersonalDataForm(request.form)
    if 'editar_detalles_personales' in request.form and form.validate():
        identificador = request.form['identificador']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        fecha = request.form['fecha']
        sexo = request.form['sexo']
        altura = request.form['altura']
        peso = request.form['peso']
        password = form.password.data
        if identificador != "":
            paciente.identificador = identificador
        if nombre != "":
            paciente.nombre = nombre
        if apellidos != "":
            paciente.apellidos = apellidos
        if fecha != "":
            paciente.fecha_nacimiento = fecha
        if sexo != "":
            paciente.sexo = sexo
        if altura != "":
            paciente.altura = altura
        if peso != "":
            paciente.peso = peso
        if password != "":
            paciente.password = hash_password(password)
        from apps import db
        db.session.commit()
        return redirect(url_for('prefall_blueprint.detalles_personales', id=id))
        
    return render_template(
        'prefall/editar_detalles_personales.html', 
        form=form, paciente=paciente)


@blueprint.route('asociar_medico/<id>/<id_medico>', methods=['GET','POST'])
@personal_data_access()
def asociar_medico(id, id_medico):
    from apps import db
    asociacion = PacienteAsociado(id_paciente= id, id_medico=id_medico)
    db.session.add(asociacion)
    db.session.commit()

    return redirect(url_for("prefall_blueprint.detalles_personales", id=id))


@blueprint.route('desasociar_medico/<id>/<id_medico>', methods=['GET','POST'])
@personal_data_access()
def desasociar_medico(id, id_medico):
    from apps import db
    paciente = User.query.filter_by(id=id).first()
    medico = User.query.filter_by(id=id_medico).first()
    paciente.medicos_asociados.remove(medico)

    db.session.commit()

    return redirect(url_for("prefall_blueprint.detalles_personales", id=id))

### END AUXILIAR ###

### BEGIN PACIENTE ###

@blueprint.route('pantalla_principal_paciente')
@roles_accepted("paciente")
def pantalla_principal_paciente():
    tests = current_user.tests
    tests_data = [{"num_test": test.num_test, "date": test.date, 
    "medico": test.medico.nombre + " " + test.medico.apellidos 
    if test.medico and test.medico.apellidos else test.medico.nombre 
    if test.medico else ""} 
    for test in tests]


    return render_template('prefall/pantalla_principal_paciente.html',
     tests = tests, tests_data=tests_data)

@blueprint.route('ver_detalles_test/<id>/<num>', methods=['GET'])
@patient_data_access()
def ver_detalles_test(id, num):
    from apps import db
    test = Test.query.filter_by(id_paciente=id).filter_by(num_test=num).first()

    diagnosticos = db.session.query(Test, AccionesTestMedico, User).\
        join(Test, db.and_(AccionesTestMedico.num_test == Test.num_test, 
        AccionesTestMedico.id_paciente == Test.id_paciente)).\
            join(User, AccionesTestMedico.id_medico == User.id).\
                with_entities(User.nombre, AccionesTestMedico.diagnostico).\
                    filter(AccionesTestMedico.diagnostico != None).\
                        filter(Test.num_test == test.num_test).\
                            filter(Test.id_paciente == test.id_paciente).all()
    return render_template(
        'prefall/ver_detalles_test.html', test = test, diagnosticos=diagnosticos
    )

### END PACIENTE ###

### BEGIN COMMON ###

ALLOWED_EXTENSIONS = {'txt', 'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_csv(filename):
    #colnames = ["item","date", "time", "acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z", "mag_x", "mag_y", "mag_z"]
    colnames = ["item","time", "frame", "acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z", "mag_x", "mag_y", "mag_z",
    "lacc_x", "lacc_y", "lacc_z", "quat_x", "quat_y", "quat_z", "quat_w"]
    df = pd.read_csv(
        filename, delim_whitespace=True, skiprows=5, usecols=range(0,19), 
        names=colnames)
    return df

def add_columns(df, id_paciente):
    df["id_paciente"] = id_paciente
    
    from apps import db
    
    test = db.session.query(Test).filter(
        Test.id_paciente == id_paciente).order_by(
        db.desc(Test.num_test)).limit(1).first()
    if test is None:
        next_num = 0
    else:
        next_num = test.num_test + 1
    df["num_test"] = next_num
    
    if not df["item"].is_unique:
        items = range(len(df.index))
        df["item"] = items

    return df

def add_df_to_sql(df, id_centro, filename):
    from apps import db
    from datetime import datetime, timedelta

    filename_without_extension = os.path.splitext(filename)[0]

    date_part, time_part = filename_without_extension.split('-', 1)

    date_obj = datetime.strptime(f"{date_part}-{time_part}", "%Y%m%d-%H-%M-%S-%f")

    formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
    print(formatted_date)

    test = Test(
        num_test = df.at[0,"num_test"], id_paciente= df.at[0,"id_paciente"],
        date = date_obj, id_centro=id_centro, id_medico= current_user.id)
    db.session.add(test)

    db.session.commit()

    test_units = []

    for index, row in df.iterrows():
        test_unit_data = {
            'item': row.at['item'],
            'num_test': row.at['num_test'],
            'id_paciente': row.at['id_paciente'],
            'time': row.at['time'],
            'acc_x': row.at['acc_x'],
            'acc_y': row.at['acc_y'],
            'acc_z': row.at['acc_z'],
            'gyr_x': row.at['gyr_x'],
            'gyr_y': row.at['gyr_y'],
            'gyr_z': row.at['gyr_z'],
            'mag_x': row.at['mag_x'],
            'mag_y': row.at['mag_y'],
            'mag_z': row.at['mag_z'],
            'lacc_x': row.at['lacc_x'],
            'lacc_y': row.at['lacc_y'],
            'lacc_z': row.at['lacc_z'],
            'quat_x': row.at['quat_x'],
            'quat_y': row.at['quat_y'],
            'quat_z': row.at['quat_z'],
            'quat_w': row.at['quat_w'],
        }
        test_units.append(test_unit_data)

    db.session.bulk_insert_mappings(TestUnit, test_units)
    
    db.session.commit()

@blueprint.route('debug/<info>')
def debug(info):
    return info

@blueprint.route("/get_test/<paciente>/<test>")
def get_test(paciente, test):
    from apps import db
    query = db.session.query(
        TestUnit.item, Test.num_test, Test.id_paciente, Test.date, TestUnit.time, TestUnit.acc_x,
        TestUnit.acc_y, TestUnit.acc_z, TestUnit.gyr_x, TestUnit.gyr_y, TestUnit.gyr_z,
        TestUnit.mag_x, TestUnit.mag_y, TestUnit.mag_z,
        TestUnit.lacc_x, TestUnit.lacc_y, TestUnit.lacc_z,
        TestUnit.quat_x, TestUnit.quat_y, TestUnit.quat_z, TestUnit.quat_w).\
                        filter(Test.id_paciente == TestUnit.id_paciente).\
                            filter(Test.num_test == TestUnit.num_test).\
                                filter(Test.id_paciente==paciente).\
                                    filter(Test.num_test==test)
    df = pd.read_sql(query.statement, db.session.bind)
    csv = df.to_csv()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=test.csv"})

@blueprint.route("/test_data/<paciente>/<test>")
def test_data(paciente, test):
    from apps import db
    query = db.session.query(
        Test.num_test, Test.id_paciente, Test.date, TestUnit.item, TestUnit.time, TestUnit.acc_x,
        TestUnit.acc_y, TestUnit.acc_z, TestUnit.gyr_x, TestUnit.gyr_y, TestUnit.gyr_z,
        TestUnit.mag_x, TestUnit.mag_y, TestUnit.mag_z, 
        TestUnit.lacc_x, TestUnit.lacc_y, TestUnit.lacc_z,
        TestUnit.quat_x, TestUnit.quat_y, TestUnit.quat_z, TestUnit.quat_w).\
                        filter(Test.id_paciente == TestUnit.id_paciente).\
                            filter(Test.num_test == TestUnit.num_test).\
                                filter(Test.id_paciente==paciente).\
                                    filter(Test.num_test==test)
    df = pd.read_sql(query.statement, db.session.bind)
    data = {
        "item": df["item"].to_list(),
        "acc_x": df["acc_x"].to_list(),
        "acc_y": df["acc_y"].to_list(),
        "acc_z": df["acc_z"].to_list(),
        "gyr_x": df["gyr_x"].to_list(),
        "gyr_y": df["gyr_y"].to_list(),
        "gyr_z": df["gyr_z"].to_list(),
        "mag_x": df["mag_x"].to_list(),
        "mag_y": df["mag_y"].to_list(),
        "mag_z": df["mag_z"].to_list(),
        "lacc_x": df["lacc_x"].to_list(),
        "lacc_y": df["lacc_y"].to_list(),
        "lacc_z": df["lacc_z"].to_list(),
        "quat_x": df["quat_x"].to_list(),
        "quat_y": df["quat_y"].to_list(),
        "quat_z": df["quat_z"].to_list(),
        "quat_w": df["quat_w"].to_list(),
    }
    return jsonify(data)

## END COMON ##

## BEGIN FLASK CKEDITOR ##

@blueprint.route('/files/<id>')
def uploaded_files(id):
    #path = current_app.config['UPLOADED_PATH']
    #return send_from_directory(path, filename)
    file = File.query.filter_by(id=id).first()
    return send_file(BytesIO(file.data), attachment_filename=file.filename)

@blueprint.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    from apps import db
    upload = File(filename=f.filename, data=f.read())
    db.session.add(upload)
    db.session.commit()
    #f.save(os.path.join(current_app.config['UPLOADED_PATH'], f.filename))
    url = url_for('prefall_blueprint.uploaded_files', id=upload.id)
    return upload_success(url, filename=f.filename)

## END FLASK CKEDITOR ##

## BEGIN PLOTS ##

@blueprint.route('/plots',  methods=['GET','POST'])
@roles_accepted("medico")
def plots():
    pacientes = current_user.pacientes_asociados.all()

    pacientes_data = [{"id": paciente.id, "apellidos": paciente.apellidos, 
    "nombre": paciente.nombre, "identificador": paciente.identificador, 
    "centro": paciente.centro.nombreFiscal} for paciente in pacientes]

    return render_template(
        'prefall/plots.html', 
        pacientes=pacientes_data)

@blueprint.route('/plots/generar_paciente/<id>', methods=['GET'])
@roles_accepted("medico")
def generate_plots_paciente(id):
    import plotly
    import plotly.graph_objs as go
    from apps import db
    import pickle
    import math
    import numpy as np
    
    tests = db.session.query(
        Test.num_test, Test.date, Test.probabilidad_caida, Test.data)\
        .filter_by(id_paciente=id)\
        .filter(Test.probabilidad_caida.isnot(None)).all()
    
    x = [test.date for test in tests]
    y = [test.probabilidad_caida * 100 for test in tests]
    
    fig = go.Figure()
    
    trace = go.Scatter(x=x, y=y, mode='lines+markers')

    fig.add_trace(trace)

    fig.update_xaxes(title_text='Fecha')
    fig.update_yaxes(title_text='Probabilidad de caída', range=[0, 100])

    #graphEvolucionProbCaida = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphEvolucionProbCaida = fig.to_dict()

    mean_acc_x = []
    mean_acc_y = []
    mean_acc_z = []

    mean_gyr_x = []
    mean_gyr_y = []
    mean_gyr_z = []

    mean_mag_x = []
    mean_mag_y = []
    mean_mag_z = []

    probs_caida = []

    for test in tests:
        """
        rows = TestUnit.query.filter_by(num_test=test.num_test).all()

        
        acc_x_values = [row.acc_x for row in rows]
        acc_y_values = [row.acc_y for row in rows]
        acc_z_values = [row.acc_z for row in rows]

        gyr_x_values = [row.gyr_x for row in rows]
        gyr_y_values = [row.gyr_y for row in rows]
        gyr_z_values = [row.gyr_z for row in rows]

        mag_x_values = [row.mag_x for row in rows]
        mag_y_values = [row.mag_y for row in rows]
        mag_z_values = [row.mag_z for row in rows]

        mean_acc_x.append(np.mean(acc_x_values))
        mean_acc_y.append(np.mean(acc_y_values))
        mean_acc_z.append(np.mean(acc_z_values))

        mean_gyr_x.append(np.mean(gyr_x_values))
        mean_gyr_y.append(np.mean(gyr_y_values))
        mean_gyr_z.append(np.mean(gyr_z_values))

        mean_mag_x.append(np.mean(mag_x_values))
        mean_mag_y.append(np.mean(mag_y_values))
        mean_mag_z.append(np.mean(mag_z_values))
        """
        data_query = db.session.query(
            TestUnit.acc_x, TestUnit.acc_y, TestUnit.acc_z,
            TestUnit.gyr_x, TestUnit.gyr_y, TestUnit.gyr_z,
            TestUnit.mag_x, TestUnit.mag_y, TestUnit.mag_z,
        ).filter_by(num_test=test.num_test).all()

        mean_values = np.mean(data_query, axis=0)

        mean_acc_x.append(mean_values[0])
        mean_acc_y.append(mean_values[1])
        mean_acc_z.append(mean_values[2])
        mean_gyr_x.append(mean_values[3])
        mean_gyr_y.append(mean_values[4])
        mean_gyr_z.append(mean_values[5])
        mean_mag_x.append(mean_values[6])
        mean_mag_y.append(mean_values[7])
        mean_mag_z.append(mean_values[8])

        probs_caida.append(test.probabilidad_caida * 100)


    print("after loop data extraction")
    
    fig = go.Figure()

    trace = go.Scatter3d(
        x=mean_acc_x,
        y=mean_acc_y,
        z=mean_acc_z,
        mode='markers',
        marker=dict(
            size=5, 
            color=probs_caida, 
            colorscale='Viridis', 
            colorbar=dict(len=1, y=0, yanchor='bottom'),  
            opacity=1, 
        )
    )

    fig.add_trace(trace)

    fig.update_scenes(xaxis_title='Aceleracion X', yaxis_title='Aceleracion Y', zaxis_title='Aceleracion Z')
    
    if len(mean_acc_x) > 0:
        x_floor = math.floor(min(mean_acc_x))
        x_ceil = math.ceil(max(mean_acc_x))

        y_floor = math.floor(min(mean_acc_y))
        y_ceil = math.ceil(max(mean_acc_y))

        z_floor = math.floor(min(mean_acc_z))
        z_ceil = math.ceil(max(mean_acc_z))

        fig.update_layout(scene=dict(
            xaxis=dict(range=[x_floor, x_ceil]),
            yaxis=dict(range=[y_floor, y_ceil]),
            zaxis=dict(range=[z_floor, z_ceil]),
        ))

    #graph3DProbCaidaAcc = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graph3DProbCaidaAcc = fig.to_dict()

    fig = go.Figure()

    trace = go.Scatter3d(
        x=mean_gyr_x,
        y=mean_gyr_y,
        z=mean_gyr_z,
        mode='markers',
        marker=dict(
            size=5, 
            color=probs_caida, 
            colorscale='Viridis', 
            colorbar=dict(len=1, y=0, yanchor='bottom'),  
            opacity=1, 
        )
    )

    fig.add_trace(trace)

    fig.update_scenes(xaxis_title='Gyroscopio X', yaxis_title='Gyroscopio Y', zaxis_title='Gyroscopio Z')
    
    if len(mean_gyr_x) > 0:
        x_floor = math.floor(min(mean_gyr_x))
        x_ceil = math.ceil(max(mean_gyr_x))

        y_floor = math.floor(min(mean_gyr_y))
        y_ceil = math.ceil(max(mean_gyr_y))

        z_floor = math.floor(min(mean_gyr_z))
        z_ceil = math.ceil(max(mean_gyr_z))

        fig.update_layout(scene=dict(
            xaxis=dict(range=[x_floor, x_ceil]),
            yaxis=dict(range=[y_floor, y_ceil]),
            zaxis=dict(range=[z_floor, z_ceil]),
        ))

    #graph3DProbCaidaGyr = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graph3DProbCaidaGyr = fig.to_dict()

    fig = go.Figure()

    trace = go.Scatter3d(
        x=mean_mag_x,
        y=mean_mag_y,
        z=mean_mag_z,
        mode='markers',
        marker=dict(
            size=5, 
            color=probs_caida, 
            colorscale='Viridis', 
            colorbar=dict(len=1, y=0, yanchor='bottom'),  
            opacity=1, 
        )
    )

    fig.add_trace(trace)

    fig.update_scenes(xaxis_title='Magnetometro X', yaxis_title='Magnetometro Y', zaxis_title='Magnetometro Z')
    
    if len(mean_mag_x) > 0:
        x_floor = math.floor(min(mean_mag_x))
        x_ceil = math.ceil(max(mean_mag_x))

        y_floor = math.floor(min(mean_mag_y))
        y_ceil = math.ceil(max(mean_mag_y))

        z_floor = math.floor(min(mean_mag_z))
        z_ceil = math.ceil(max(mean_mag_z))

        fig.update_layout(scene=dict(
            xaxis=dict(range=[x_floor, x_ceil]),
            yaxis=dict(range=[y_floor, y_ceil]),
            zaxis=dict(range=[z_floor, z_ceil]),
        ))

    #graph3DProbCaidaMag = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graph3DProbCaidaMag = fig.to_dict()

    return jsonify({
        "prob_caida": graphEvolucionProbCaida,
        "acelerometro": graph3DProbCaidaAcc,
        "giroscopio": graph3DProbCaidaGyr,
        "magnetometro": graph3DProbCaidaMag
    })


@blueprint.route('/get_tests/<id_paciente>',  methods=['GET'])
@clinical_data_access()
def get_tests(id_paciente):
    from apps import db
    from sqlalchemy.orm import aliased

    Paciente = aliased(User)
    Medico = aliased(User)

    tests = (
        db.session.query(Test, Centro, Paciente, Medico)
        .join(Centro, Test.id_centro == Centro.id)
        .join(Paciente, Test.id_paciente == Paciente.id)
        .outerjoin(Medico, Test.id_medico == Medico.id)
        .filter(Test.id_paciente == id_paciente)
        .all()
    )
    tests_data = [{"num_test": test.Test.num_test, "id_paciente":test.Test.id_paciente,
     "date": test.Test.date} for test in tests]
    return jsonify(tests_data)

@blueprint.route('/plots/get_test_data/<id_paciente>/<num_test>', methods=['GET'])
@clinical_data_access()
def get_data(id_paciente, num_test):
    from apps import db
    import pickle
    import numpy as np
    paciente = db.session.query(
        User.nombre, User.apellidos)\
        .filter_by(id=id_paciente).first()
    test = db.session.query(
        Test.num_test, Test.date, Test.probabilidad_caida, Test.data)\
        .filter_by(id_paciente=id_paciente)\
        .filter(Test.num_test==num_test).first()
    fases = None
    blob_data = test.data  
    if blob_data:
        df = pickle.loads(blob_data)
        fases = {
            'fase1': df['duracion_f1'].values[0],
            'fase2': df['duracion_f2'].values[0],
            'fase3': df['duracion_f3'].values[0],
            'fase4': df['duracion_f4'].values[0]
        }
    test_data = db.session.query(
            TestUnit.acc_x, TestUnit.acc_y, TestUnit.acc_z,
            TestUnit.gyr_x, TestUnit.gyr_y, TestUnit.gyr_z,
            TestUnit.mag_x, TestUnit.mag_y, TestUnit.mag_z,
        ).filter_by(num_test=test.num_test).all()
    
    mean_values = np.mean(test_data, axis=0)

    acc = {"x": mean_values[0], "y": mean_values[1], "z":mean_values[2]}
    gyr = {"x": mean_values[3], "y": mean_values[4], "z":mean_values[5]}
    mag = {"x": mean_values[6], "y": mean_values[7], "z":mean_values[8]}

    full_name = paciente.nombre + (" " + paciente.apellidos if paciente.apellidos else "")
    data = {"fases": fases, "acc": acc, "gyr": gyr, "mag": mag,
    "full_name":full_name, "date": test.date}
    return jsonify(data)


@blueprint.route('/get_paciente_tests', methods=['POST'])
def get_paciente_tests():
    from apps import db
    id_paciente = request.form.get('id_paciente') 
    
    tests = db.session.query(Test.num_test, Test.date).\
    filter_by(id_paciente=id_paciente).\
    filter(Test.probabilidad_caida.isnot(None)).all()
    
    tests_data = []
    for test in tests:
        test_dict = {
            'num_test': test.num_test,
            'date': test.date,
        }
        tests_data.append(test_dict)

    response_data = {'tests': tests_data}

    return jsonify(response_data)


@blueprint.route('/plots_paciente',  methods=['GET','POST'])
@roles_accepted("paciente")
def plots_paciente():
    import plotly
    import plotly.graph_objs as go
    from apps import db

    tests = db.session.query(
        Test.num_test, Test.date)\
        .filter_by(id_paciente=current_user.id).all()
    tests_data = [{"num_test": test.num_test,
     "date": test.date} for test in tests]


    tests = db.session.query(
        Test.num_test, Test.date, Test.probabilidad_caida, Test.data)\
        .filter_by(id_paciente=current_user.id)\
        .filter(Test.probabilidad_caida.isnot(None)).all()
    
    x = [test.date for test in tests]
    y = [test.probabilidad_caida * 100 for test in tests]
    
    fig = go.Figure()
    
    trace = go.Scatter(x=x, y=y, mode='lines+markers')

    fig.add_trace(trace)

    fig.update_xaxes(title_text='Fecha')
    fig.update_yaxes(title_text='Probabilidad de caída', range=[0, 100])

    graphEvolucionProbCaida = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        'prefall/plots_paciente.html', 
        tests_data=tests_data,
        graphEvolucionProbCaida=graphEvolucionProbCaida)

@blueprint.route('/obtener_centros', methods=['GET'])
def obtener_centros():
    from apps import db
    centers = Centro.query.order_by(Centro.nombreFiscal).all()

    centros_list = [{"id": centro.id, "nombre": centro.nombreFiscal} for centro in centers]

    return jsonify({"centros": centros_list})

@blueprint.route('/plots/generar_tests/<id>', methods=['POST'])
@patient_data_access()
def generar_tests(id):
    from apps import db
    import pickle
    import numpy as np
    import plotly
    import plotly.graph_objs as go
    data = request.get_json()
    test_nums = data.get('tests')
    paciente = db.session.query(
        User.nombre, User.apellidos)\
        .filter_by(id=id).first()
    tests = db.session.query(
        Test.num_test, Test.date, Test.probabilidad_caida, Test.data)\
        .filter_by(id_paciente=id)\
        .filter(Test.num_test.in_(test_nums)).all()

    acc_data = []
    gyr_data = []
    mag_data = []
    dates_data = []
    fases_data = []
    dates_fases_data = []

    graphDataAcc = []
    layout = go.Layout(
        barmode='group',
        title='Comparación de la aceleración',
        xaxis=dict(title='Eje'),
        yaxis=dict(title='Aceleración media')
    )
    figAcc = go.Figure()
    figAcc.update_layout(
        title="Comparación del acelerómetro",
    )
    figGyr = go.Figure()
    figGyr.update_layout(
        title="Comparación del giroscopio",
    )
    figMag = go.Figure()
    figMag.update_layout(
        title="Comparación del magnetómetro",
    )
    figFases = go.Figure()
    figFases.update_layout(
        title="Duración de las fases de la marcha",
    )
    for test in tests:
        fases = None
        blob_data = test.data  
        if blob_data:
            df = pickle.loads(blob_data)
            fases = {
                'fase1': df['duracion_f1'].values[0],
                'fase2': df['duracion_f2'].values[0],
                'fase3': df['duracion_f3'].values[0],
                'fase4': df['duracion_f4'].values[0]
            }
            trace_fases = go.Bar(
                x=["Fase 1", "Fase 2", "Fase 3", "Fase 4"],
                y=[fases['fase1'], fases['fase2'], fases['fase3'], fases['fase4']],
                name=test['date'].strftime("%Y-%m-%d %H:%M:%S")
            )
            figFases.add_trace(trace_fases)
        test_data = db.session.query(
                TestUnit.acc_x, TestUnit.acc_y, TestUnit.acc_z,
                TestUnit.gyr_x, TestUnit.gyr_y, TestUnit.gyr_z,
                TestUnit.mag_x, TestUnit.mag_y, TestUnit.mag_z,
            ).filter_by(num_test=test.num_test).all()
        
        mean_values = np.mean(test_data, axis=0)

        acc = {"x": mean_values[0], "y": mean_values[1], "z":mean_values[2]}
        gyr = {"x": mean_values[3], "y": mean_values[4], "z":mean_values[5]}
        mag = {"x": mean_values[6], "y": mean_values[7], "z":mean_values[8]}
        trace_acc = go.Bar(
            x=["Aceleracion X", "Aceleracion Y", "Aceleracion Z"],
            y=[acc['x'], acc['y'], acc['z']],
            name=test['date'].strftime("%Y-%m-%d %H:%M:%S")
        )
        figAcc.add_trace(trace_acc)
        trace_gyr = go.Bar(
            x=["Giroscopio X", "Giroscopio Y", "Giroscopio Z"],
            y=[gyr['x'], gyr['y'], gyr['z']],
            name=test['date'].strftime("%Y-%m-%d %H:%M:%S")
        )
        figGyr.add_trace(trace_gyr)
        trace_mag = go.Bar(
            x=["Magnetometro X", "Magnetometro Y", "Magnetometro Z"],
            y=[mag['x'], mag['y'], mag['z']],
            name=test['date'].strftime("%Y-%m-%d %H:%M:%S")
        )
        figMag.add_trace(trace_mag)

    
    #plotAcc = json.dumps(figAcc, cls=plotly.utils.PlotlyJSONEncoder)
    plotAcc = figAcc.to_dict()
    plotGyr = figGyr.to_dict()
    plotMag = figMag.to_dict()
    plotFases = figFases.to_dict()
    return jsonify({"plotAcc": plotAcc, "plotGyr": plotGyr, "plotMag": plotMag, "plotFases": plotFases})


@blueprint.route('/plots/generar_tests_medico/', methods=['POST'])
@roles_accepted("medico")
def generar_tests_medico():
    from apps import db
    import pickle
    import numpy as np
    import plotly
    import plotly.graph_objs as go
    from sqlalchemy.orm import joinedload
    data = request.get_json()
    tests_data = data.get('tests')
    tests = []
    for test in tests_data:
        id_paciente = test.get('paciente')
        num_test = test.get('test')
        specific_test = db.session.query(Test) \
            .filter(Test.num_test == num_test, Test.id_paciente == id_paciente) \
            .options(joinedload(Test.paciente)) \
            .first()
        tests.append(specific_test)

    acc_data = []
    gyr_data = []
    mag_data = []
    dates_data = []
    fases_data = []
    dates_fases_data = []

    graphDataAcc = []
    layout = go.Layout(
        barmode='group',
        title='Comparación de la aceleración',
        xaxis=dict(title='Eje'),
        yaxis=dict(title='Aceleración media')
    )
    figAcc = go.Figure()
    figAcc.update_layout(
        title="Comparación del acelerómetro",
    )
    figGyr = go.Figure()
    figGyr.update_layout(
        title="Comparación del giroscopio",
    )
    figMag = go.Figure()
    figMag.update_layout(
        title="Comparación del magnetómetro",
    )
    figFases = go.Figure()
    figFases.update_layout(
        title="Duración de las fases de la marcha",
    )
    for test in tests:
        fases = None
        blob_data = test.data  
        if blob_data:
            df = pickle.loads(blob_data)
            fases = {
                'fase1': df['duracion_f1'].values[0],
                'fase2': df['duracion_f2'].values[0],
                'fase3': df['duracion_f3'].values[0],
                'fase4': df['duracion_f4'].values[0]
            }
            trace_fases = go.Bar(
                x=["Fase 1", "Fase 2", "Fase 3", "Fase 4"],
                y=[fases['fase1'], fases['fase2'], fases['fase3'], fases['fase4']],
                name=test.paciente.nombre + " " + test.paciente.apellidos + " " + test.date.strftime("%Y-%m-%d %H:%M:%S")
            )
            figFases.add_trace(trace_fases)
        test_data = db.session.query(
                TestUnit.acc_x, TestUnit.acc_y, TestUnit.acc_z,
                TestUnit.gyr_x, TestUnit.gyr_y, TestUnit.gyr_z,
                TestUnit.mag_x, TestUnit.mag_y, TestUnit.mag_z,
            ).filter_by(num_test=test.num_test).all()
        
        mean_values = np.mean(test_data, axis=0)

        acc = {"x": mean_values[0], "y": mean_values[1], "z":mean_values[2]}
        gyr = {"x": mean_values[3], "y": mean_values[4], "z":mean_values[5]}
        mag = {"x": mean_values[6], "y": mean_values[7], "z":mean_values[8]}
        trace_acc = go.Bar(
            x=["Aceleracion X", "Aceleracion Y", "Aceleracion Z"],
            y=[acc['x'], acc['y'], acc['z']],
            name=test.paciente.nombre + " " + test.paciente.apellidos + " " + test.date.strftime("%Y-%m-%d %H:%M:%S")
        )
        figAcc.add_trace(trace_acc)
        trace_gyr = go.Bar(
            x=["Giroscopio X", "Giroscopio Y", "Giroscopio Z"],
            y=[gyr['x'], gyr['y'], gyr['z']],
            name=test.paciente.nombre + " " + test.paciente.apellidos + " " + test.date.strftime("%Y-%m-%d %H:%M:%S")
        )
        figGyr.add_trace(trace_gyr)
        trace_mag = go.Bar(
            x=["Magnetometro X", "Magnetometro Y", "Magnetometro Z"],
            y=[mag['x'], mag['y'], mag['z']],
            name=test.paciente.nombre + " " + test.paciente.apellidos + " " + test.date.strftime("%Y-%m-%d %H:%M:%S")
        )
        figMag.add_trace(trace_mag)

    
    #plotAcc = json.dumps(figAcc, cls=plotly.utils.PlotlyJSONEncoder)
    plotAcc = figAcc.to_dict()
    plotGyr = figGyr.to_dict()
    plotMag = figMag.to_dict()
    plotFases = figFases.to_dict()
    return jsonify({"plotAcc": plotAcc, "plotGyr": plotGyr, "plotMag": plotMag, "plotFases": plotFases})

    

        
