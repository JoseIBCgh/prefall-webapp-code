from sqlite3 import IntegrityError
from sqlalchemy import null, desc, create_engine, exc, cast
import sqlalchemy

from io import BytesIO

from apps.authentication.models import AccionesTestMedico, DocumentoPaciente, PacienteAsociado, Role, Test, TestUnit, User, Centro, File
from apps.prefall import blueprint
from flask import abort, jsonify, render_template, request, redirect, url_for, send_file
from jinja2 import TemplateNotFound

from flask_security import (
    auth_required,
    roles_accepted,
    hash_password,
    current_user
)
from random import randint

from flask import flash, current_app, Response
from werkzeug.utils import secure_filename
import os
from pathlib import Path

from apps.prefall.decorators import admin_centro_access, clinical_data_access, patient_data_access, personal_data_access
from apps.prefall.forms import (
    CreateCenterAdminForm,
    CreateCenterForm,
    CreatePatientClinicalForm,
    CreatePatientPersonalForm,
    DiagnosticarTestForm,
    EditCenterDataForm, 
    EditClinicalDataForm, 
    EditPersonalDataForm,
    FilterFileForm,
    FilterTestForm,
    FilterUserForm,
    UploadFileForm,
    UploadTestForm,
)

import csv
import pandas as pd

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
    

    return render_template('prefall/center_list.html', centros=centros)


@blueprint.route('detalles_centro_admin/<id>', methods=['GET', 'POST'])
@roles_accepted("admin")
def detalles_centro_admin(id):
    from apps import db
    centro = Centro.query.filter_by(id=id).first()
    users = User.query.filter_by(id_centro=id).filter(Centro.id == id).\
        filter(db.or_(Centro.id_admin == None,Centro.id_admin != User.id)).all()
    admin = User.query.filter_by(id_centro=id).filter(Centro.id == id).\
        filter(Centro.id_admin == User.id).first()

    return render_template(
        'prefall/detalles_centro_admin.html', centro=centro, users=users, admin=admin)


@blueprint.route('crear_admin_centro/<id>', methods=['GET', 'POST'])
@roles_accepted("admin")
def crear_admin_centro(id):
    centro = Centro.query.filter_by(id=id).first()
    form = CreateCenterAdminForm()
    if form.validate_on_submit():
        username = form["username"].data
        password = form["password"].data
        email = form["email"].data
        from apps import user_datastore, db
        user_datastore.create_user(
            username= username, id_centro = id,
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

    return render_template(
        'prefall/detalles_centro.html', centro=centro, users=users)


@blueprint.route('borrar_usuario/<id_centro>/<id_user>', methods=['GET','POST'])
@admin_centro_access()
def borrar_usuario(id_centro, id_user):
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

### END ADMIN CENTRO ###

### BEGIN MEDICO ###

@blueprint.route('/pantalla_principal_medico', methods=['GET', 'POST'])
@roles_accepted("medico")
def pantalla_principal_medico():
    from apps import db
    formPacientes = FilterUserForm()

    if formPacientes.submitFilterUser.data and formPacientes.validate():
        identificador = formPacientes.identificador.data
        nombre = formPacientes.nombre.data
        centro = formPacientes.centro.data
        pacientes = current_user.pacientes_asociados.\
                    filter(User.nombre.like('%'+nombre+'%')).\
                        filter(User.identificador.like('%'+identificador+'%')).\
                            filter(User.id_centro == Centro.id).\
                                filter(Centro.nombreFiscal.like('%'+centro+'%')).all()
    else:
        pacientes = current_user.pacientes_asociados

    id_asociados = [pa.id for pa in current_user.pacientes_asociados]
    formTests = FilterTestForm()
    if formTests.submitFilterTest.data and formTests.validate():
        nombre = formTests.nombrePaciente.data
        numero = formTests.numero.data
        if numero == None:
            numero = ""
        else:
            numero = str(numero)
            
        tests = current_user.tests_de_pacientes.\
            join(User, AccionesTestMedico.id_paciente == User.id).\
                join(Test, db.and_(AccionesTestMedico.num_test == Test.num_test, 
                    AccionesTestMedico.id_paciente == Test.id_paciente)).\
                        with_entities(AccionesTestMedico.visto, AccionesTestMedico.diagnostico, User.nombre, User.id, 
                        AccionesTestMedico.num_test, Test.date).\
                            filter(User.nombre.like('%'+nombre+'%')).\
                                filter(cast(Test.num_test, db.String).like('%'+numero+'%')).all()
    
    else:
        '''tests = db.session.query(Test.nuevo, Test.diagnostico, User.nombre, User.id, Test.num_test, Test.date).\
                    filter(Test.id_paciente.in_(id_asociados)).\
                        filter(Test.id_paciente == User.id).all()'''
        tests = current_user.tests_de_pacientes.\
            join(User, AccionesTestMedico.id_paciente == User.id).\
                join(Test, db.and_(AccionesTestMedico.num_test == Test.num_test, 
                    AccionesTestMedico.id_paciente == Test.id_paciente)).\
                        with_entities(AccionesTestMedico.visto, AccionesTestMedico.diagnostico, User.nombre, User.id, 
                        AccionesTestMedico.num_test, Test.date).all()
    
    '''alertas = db.session.query(Test.nuevo, Test.diagnostico, User.nombre, User.id, Test.num_test, Test.date).\
                filter(Test.id_paciente.in_(id_asociados)).\
                    filter(Test.id_paciente == User.id).\
                        filter(Test.diagnostico == None).all()'''
    test_sin_diagnosticar = current_user.tests_de_pacientes.\
        join(User, AccionesTestMedico.id_paciente == User.id).\
            join(Test, db.and_(AccionesTestMedico.num_test == Test.num_test, 
                AccionesTestMedico.id_paciente == Test.id_paciente)).\
                    with_entities(AccionesTestMedico.visto, AccionesTestMedico.diagnostico, User.nombre, User.id, 
                    AccionesTestMedico.num_test, Test.date).\
                        filter(AccionesTestMedico.diagnostico == None).all()

    test_sin_revisar = current_user.tests_de_pacientes.\
        join(User, AccionesTestMedico.id_paciente == User.id).\
            join(Test, db.and_(AccionesTestMedico.num_test == Test.num_test, 
                AccionesTestMedico.id_paciente == Test.id_paciente)).\
                    with_entities(AccionesTestMedico.visto, AccionesTestMedico.diagnostico, User.nombre, User.id, 
                    AccionesTestMedico.num_test, Test.date).\
                        filter(AccionesTestMedico.visto == False).all()
    
    return render_template(
        'prefall/pantalla_principal_medico.html', pacientes=pacientes, formPacientes=formPacientes,
        tests= tests, test_sin_diagnosticar=test_sin_diagnosticar, test_sin_revisar=test_sin_revisar,
        formTests=formTests)

@blueprint.route('crear_paciente_medico', methods=['GET', 'POST'])
@roles_accepted("medico")
def crear_paciente_medico():
    create_patient_form = CreatePatientClinicalForm(request.form)
    if 'create_patient' in request.form and create_patient_form.validate():

        # read form data
        identificador = request.form['identificador']
        nombre = request.form['nombre']
        fecha = request.form['fecha']
        sexo = request.form['sexo']
        altura = request.form['altura']
        peso = request.form['peso']
        antecedentes = request.form['antecedentes']

        default_password = "password"
        n = randint(0,1000000)
        default_email = "default"+ str(n) +"@invented_mail.com"

        from apps import user_datastore, db
        user_datastore.create_user(
            identificador=identificador, nombre=nombre, fecha_nacimiento=fecha, sexo=sexo, altura=altura,
            peso=peso, antecedentes_clinicos=antecedentes, id_centro = current_user.id_centro,
            password=hash_password(default_password), email=default_email, roles=["paciente"]
        )
        user_created = User.query.filter_by(identificador=identificador).first()
        asociacion = PacienteAsociado(id_paciente= user_created.id, id_medico=current_user.id)
        db.session.add(asociacion)
        db.session.commit()

        return redirect(url_for('home_blueprint.index'))


    return render_template('prefall/create_patient_clinical.html', form=create_patient_form)

@blueprint.route('detalles_test/<id>/<num>', methods=['GET', 'POST'])
@clinical_data_access()
def detalles_test(id, num):
    from apps import db
    test = db.session.query(Test, AccionesTestMedico).\
        join(Test, db.and_(AccionesTestMedico.num_test == Test.num_test, 
        AccionesTestMedico.id_paciente == Test.id_paciente)).\
            with_entities(AccionesTestMedico.visto, AccionesTestMedico.diagnostico, Test.num_test, 
                    Test.date, Test.id_paciente, Test.id_centro).\
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
        test = {"visto": True, "diagnostico": form.diagnostico.data, "num_test": test.num_test,
        "date": test.date, "id_paciente": test.id_paciente, "id_centro": test.id_centro}
    return render_template(
        'prefall/detalles_test.html', form = form, test = test
    )


@blueprint.route('detalles_clinicos/<id>', methods=['GET', 'POST'])
@clinical_data_access()
def detalles_clinicos(id):
    from apps import db
    paciente = User.query.filter_by(id=id).first()
    formFile = UploadFileForm()
    formFilterFile = FilterFileForm()
    formTest = UploadTestForm()

    if formFile.submitUploadFile.data and formFile.validate():
        file = formFile.file.data

        upload = File(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        documentoPaciente = DocumentoPaciente(id_paciente = id, id_medico=current_user.id, id_file=upload.id)
        db.session.add(documentoPaciente)
        db.session.commit()

    if formTest.submitUploadTest.data and formTest.validate():
        file = formTest.test.data
        filename = secure_filename(file.filename)
        Path(os.path.join(current_app.instance_path,current_app.config['UPLOAD_FOLDER'])).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(current_app.instance_path,current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        df = read_csv(file_path)
        df = add_columns(df, id)
        df = df.drop_duplicates(subset=["time"])
        add_df_to_sql(df, paciente.id_centro)
        '''
        try:
            add_df_to_sql(df)
        except sqlalchemy.exc.IntegrityError:
            form.test.errors.append("Duplicated data")
        '''

        os.remove(file_path)
    
    tests = db.session.query(Test.num_test, Test.date).filter_by(id_paciente=id).all()
    filesQuery = File.query.filter(File.id == DocumentoPaciente.id_file).\
        filter(DocumentoPaciente.id_paciente==id).filter(DocumentoPaciente.id_medico==current_user.id)
    
    if formFilterFile.submitFilterFile.data and formFilterFile.validate():
        file_name = formFilterFile.nombreFichero.data
        files = File.query.filter(File.id == DocumentoPaciente.id_file).\
            filter(DocumentoPaciente.id_paciente==id).filter(DocumentoPaciente.id_medico==current_user.id).\
                filter(File.filename.like('%'+file_name+'%')).all()
    else:
        files = File.query.filter(File.id == DocumentoPaciente.id_file).\
            filter(DocumentoPaciente.id_paciente==id).filter(DocumentoPaciente.id_medico==current_user.id).all()
    

    return render_template('prefall/detalles_clinicos.html', paciente=paciente, tests=tests, files=files,
    formFile=formFile, formTest=formTest, formFilterFile=formFilterFile)


@blueprint.route('editar_detalles_clinicos/<id>', methods=['GET', 'POST'])
@clinical_data_access()
def editar_detalles_clinicos(id):
    paciente = User.query.filter_by(id=id).first()
    form = EditClinicalDataForm(request.form)
    if 'editar_detalles_clinicos' in request.form and form.validate():
        identificador = request.form['identificador']
        nombre = request.form['nombre']
        fecha = request.form['fecha']
        sexo = request.form['sexo']
        altura = request.form['altura']
        peso = request.form['peso']
        antecedentes = request.form['antecedentes']
        if identificador != "":
            paciente.identificador = identificador
        if nombre != "":
            paciente.nombre = nombre
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

### END MEDICO ###
### BEGIN AUXILIAR ###

@blueprint.route('/pantalla_principal_auxiliar', methods=['GET', 'POST'])
@roles_accepted("auxiliar")
def pantalla_principal_auxiliar():
    from apps import db
    formPacientes = FilterUserForm()
    userRole = Role.query.filter_by(name="paciente").first()
    center = current_user.centro

    if formPacientes.submitFilterUser.data and formPacientes.validate():
        identificador = formPacientes.identificador.data
        nombre = formPacientes.nombre.data
        centroFiltro = formPacientes.centro.data
        pacientes = User.query.\
            filter(User.roles.contains(userRole)).\
                filter_by(centro = center).\
                    filter(User.nombre.like('%'+nombre+'%')).\
                        filter(User.identificador.like('%'+identificador+'%')).\
                            filter(User.id_centro == Centro.id).\
                                filter(Centro.nombreFiscal.like('%'+centroFiltro+'%')).all()
    else:
        pacientes = User.query.\
            filter(User.roles.contains(userRole)).\
                filter_by(centro = center).all()

    return render_template(
        'prefall/pantalla_principal_auxiliar.html', pacientes=pacientes, formPacientes=formPacientes)

@blueprint.route('crear_paciente', methods=['GET', 'POST'])
@roles_accepted("auxiliar")
def crear_paciente_auxiliar():
    create_patient_form = CreatePatientPersonalForm(request.form)
    if 'create_patient' in request.form and create_patient_form.validate():

        # read form data
        identificador = request.form['identificador']
        nombre = request.form['nombre']
        fecha = request.form['fecha']
        sexo = request.form['sexo']
        altura = request.form['altura']
        peso = request.form['peso']

        default_password = "password"
        n = randint(0,1000000)
        default_email = "default"+ str(n) +"@invented_mail.com"

        from apps import user_datastore, db
        user_datastore.create_user(
            identificador=identificador, nombre=nombre, fecha_nacimiento=fecha, sexo=sexo, altura=altura,
            peso=peso, id_centro = current_user.id_centro,
            password=hash_password(default_password), email=default_email, roles=["paciente"]
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

    if uploadTestForm.submitUpload.data and uploadTestForm.validate():
        file = uploadTestForm.test.data
        filename = secure_filename(file.filename)
        Path(os.path.join(current_app.instance_path,current_app.config['UPLOAD_FOLDER'])).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(current_app.instance_path,current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        df = read_csv(file_path)
        df = add_columns(df, id)
        df = df.drop_duplicates(subset=["time"])
        add_df_to_sql(df, paciente.id_centro)
        os.remove(file_path)

    rolMedico = Role.query.filter_by(name="medico").first()
    id_asociados = [ma.id for ma in medicos_asociados]
    if searchDoctorForm.submitFilterUser.data and searchDoctorForm.validate():
        identificador = searchDoctorForm.identificador.data
        nombre = searchDoctorForm.nombre.data
        medicos = User.query.\
            filter(User.roles.contains(rolMedico)).\
                filter(User.nombre.like('%'+nombre+'%')).\
                    filter(User.identificador.like( '%'+ identificador +'%' ) ).\
                        filter(db.not_(User.id.in_(id_asociados))).order_by(User.nombre).all()
    else:
        medicos = User.query.\
            filter(User.roles.contains(rolMedico)).\
                filter(db.not_(User.id.in_(id_asociados))).order_by(User.nombre).all()

    tests = db.session.query(Test.num_test, Test.date).filter_by(id_paciente=id).all()

    return render_template(
        'prefall/detalles_personales.html', paciente=paciente, medicos_asociados = medicos_asociados, 
        medicos= medicos, tests=tests, uploadTestForm=uploadTestForm, searchDoctorForm=searchDoctorForm)


@blueprint.route('editar_detalles_personales/<id>', methods=['GET', 'POST'])
@personal_data_access()
def editar_detalles_personales(id):
    paciente = User.query.filter_by(id=id).first()
    form = EditPersonalDataForm(request.form)
    if 'editar_detalles_personales' in request.form and form.validate():
        identificador = request.form['identificador']
        nombre = request.form['nombre']
        fecha = request.form['fecha']
        sexo = request.form['sexo']
        altura = request.form['altura']
        peso = request.form['peso']
        if identificador != "":
            paciente.identificador = identificador
        if nombre != "":
            paciente.nombre = nombre
        if fecha != "":
            paciente.fecha_nacimiento = fecha
        if sexo != "":
            paciente.sexo = sexo
        if altura != "":
            paciente.altura = altura
        if peso != "":
            paciente.peso = peso
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

    return render_template('prefall/pantalla_principal_paciente.html', tests = tests)

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
    colnames = ["item","date", "time", "acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z", "mag_x", "mag_y", "mag_z"]
    df = pd.read_csv(
        filename, delim_whitespace=True, skiprows=6, usecols=range(0,12), 
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

def add_df_to_sql(df, id_centro):
    from apps import db

    test = Test(
        num_test = df.at[0,"num_test"], id_paciente= df.at[0,"id_paciente"],
        date = df.at[0,"date"], id_centro=id_centro)
    db.session.add(test)

    for index, row in df.iterrows():
        testUnit = TestUnit(
            item = row.at["item"],
            num_test = row.at["num_test"], id_paciente= row.at["id_paciente"], time= row.at["time"],
            acc_x = row.at["acc_x"], acc_y = row.at["acc_y"], acc_z = row.at["acc_z"],
            gyr_x = row.at["gyr_x"], gyr_y = row.at["gyr_y"], gyr_z = row.at["gyr_z"],
            mag_x = row.at["mag_x"], mag_y = row.at["mag_y"], mag_z = row.at["mag_z"]
        )
        db.session.add(testUnit)
    
    db.session.commit()

@blueprint.route('debug/<info>')
def debug(info):
    return info

@blueprint.route("/get_test/<paciente>/<test>")
def get_test(paciente, test):
    from apps import db
    query = db.session.query(
        Test.num_test, Test.id_paciente, Test.date, TestUnit.time, TestUnit.acc_x,
        TestUnit.acc_y, TestUnit.acc_z, TestUnit.gyr_x, TestUnit.gyr_y, TestUnit.gyr_z,
        TestUnit.mag_x, TestUnit.mag_y, TestUnit.mag_z).\
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
        TestUnit.mag_x, TestUnit.mag_y, TestUnit.mag_z).\
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
    }
    return jsonify(data)